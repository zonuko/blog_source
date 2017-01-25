Programming Phoenix勉強その11
################################

:date: 2017-01-27 22:21
:tags: Elixir,Phoenix
:slug: programming-phoenix11
:related_posts: programming-phoenix10, programming-phoenix7
:summary: Programming Phoenixって本を読むその11

その11です。chapter8です。テストですよ

環境が ``test`` になるのでChapter7でやったWindows用コンパイルをやっておきます。細かい部分は省きます。

.. code-block:: shell
  :linenos:

  rumbl> set "MIX_ENV=test" && mix deps.compile

============================================
テスト用に自動生成されるコードについて
============================================

テストを実行する前に自動生成された ``video_controller_test.exs`` を削除しておきます。

``conn_case.ex`` を見るとテストの初期設定がかいてあるっぽいです。ちなみに最新版だと書籍のやつと大分違います。

.. code-block:: Elixir
  :linenos:


  defmodule Rumbl.ConnCase do
    use ExUnit.CaseTemplate
  
    using do
      quote do
        # Import conveniences for testing with connections
        use Phoenix.ConnTest
  
        alias Rumbl.Repo
        import Ecto
        import Ecto.Changeset
        import Ecto.Query
  
        import Rumbl.Router.Helpers
  
        # The default endpoint for testing
        @endpoint Rumbl.Endpoint
      end
    end
  
    setup tags do
      :ok = Ecto.Adapters.SQL.Sandbox.checkout(Rumbl.Repo)
  
      unless tags[:async] do
        Ecto.Adapters.SQL.Sandbox.mode(Rumbl.Repo, {:shared, self()})
      end
  
      {:ok, conn: Phoenix.ConnTest.build_conn()}
    end
  end

| ``using`` ブロックは対して違いが無いですが、 ``setup`` ブロックは大分違います。 `Ectoのドキュメント <https://hexdocs.pm/ecto/Ecto.Adapters.SQL.Sandbox.html>`_ を見て探ってみます。 
| ``Ecto.Adapters.SQL.Sandbox.checkout(Rumbl.Repo)`` では与えられたリポジトリに対してコネクションを取りに行っているようです。
| 次の ``Ecto.Adapters.SQL.Sandbox.mode(Rumbl.Repo, {:shared, self()})`` は接続の共有方法を指定しているようです。同期的にテストを行う場合はこちらのようです。（ ``allow/3`` 関数を使った非同期の方も書いてありましたが割愛します。）
| また、これは ``checkout`` された接続と同じ接続を使うようなので ``checkout`` の後に呼び出すのが必須なようです。
| 接続に対して所有権の概念が導入されこのようになったようです。
|
| 
  
============================================
ログアウト時のテストの実装
============================================

まずテストデータを作る関数を作ります。 ``test/support/test_helpers.ex`` を作ります。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.TestHelpers do
    alias Rumbl.Repo
  
    def insert_user(attrs \\ %{}) do
      # Dictをマージする キーが被っている時は第二引数のものが優先される
      changes = Enum.into(attrs, %{
        name: "Some User",
        username: "user#{Base.encode16(:crypto.rand_bytes(8))}",
        password: "supersecret",
      })
  
      %Rumbl.User{}
      |> Rumbl.User.registration_changeset(changes)
      |> Repo.insert!()
    end
  
    def insert_video(user, attrs \\ %{}) do
      user
      |> Ecto.build_assoc(:videos, attrs)
      |> Repo.insert!()
    end
  end

新しい目のElixirだと ``Dict`` がdeprecatedと怒られるので ``Enum.into`` に変えてます。第一引数の ``Enumerable`` を第二引数の ``Collectable`` のものに合体します。パイプでやろうかと思いましたが逆に見にくくなりそうだったのでやめました。

作った関数を各テストで使えるように ``import`` します。

.. code-block:: Elixir
  :linenos:

  using do
    quote do
      # Import conveniences for testing with connections
      use Phoenix.ConnTest

      alias Rumbl.Repo
      import Ecto
      import Ecto.Changeset
      import Ecto.Query

      import Rumbl.Router.Helpers
      # 自分で実装したヘルパー関数を各テストで使えるようにする
      import Rumbl.TestHelpers

      # The default endpoint for testing
      @endpoint Rumbl.Endpoint
    end
  end

最後に ``video_controller_test.exs`` を作ります。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.VideoControllerTest do
    use Rumbl.ConnCase
  
    test "requires user authentication on all actions", %{conn: conn} do
      Enum.each([
        get(conn, video_path(conn, :new)),
        get(conn, video_path(conn, :index)),
        get(conn, video_path(conn, :show, "123")),
        get(conn, video_path(conn, :edit, "123")),
        put(conn, video_path(conn, :update, "123", %{})),
        post(conn, video_path(conn, :create, %{})),
        delete(conn, video_path(conn, :delete, "123")),
      ], fn conn ->
        assert html_response(conn, 302) # ユーザ認証が必要なので全部設定されたパスにリダイレクトされる
        assert conn.halted # 認証が行われていないのでhaltedはtrueになる
      end)
    end
  end

ユーザ認証が行われていない時にちゃんとリダイレクトされて ``halted`` が ``true`` になっているかテストをしています。このテストは ``mix test`` で実行した時にパスするはずです。


============================================
ログイン時のテストの実装
============================================

ログアウトときたらログインということで実装してみます。

まずテスト時にログインしてないと話にならないのでそこら辺からやっていきます。 ``auth.ex`` の ``call/2`` 関数を変更します。

.. code-block:: Elixir
  :linenos:

  def call(conn, repo) do
    user_id = get_session(conn, :user_id)
    cond do
      user = conn.assigns[:current_user] ->
        conn
      user = user_id && repo.get(Rumbl.User, user_id) ->
        # assignでconnを変更する(importされた関数)
        # これによって:current_userがコントローラやビューで使えるようになる
        assign(conn, :current_user, user)
      true ->
        assign(conn, :current_user, nil)
    end
  end

``cond`` で場合分けをしていて、カレントユーザがすでに入ればそのまま ``conn`` を返します。これで ``:current_user`` を突っ込んだ後にこいつを呼び出せばそのまま処理に移れるはずです。

次に ``video_controller_test.exs`` に以下を追加します。
