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
テストの実装
============================================

まずテストデータを作る関数を作ります。 ``test/support/test_helpers.ex`` を作ります。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.TestHelpers do
    alias Rumbl.Repo
  
    def insert_user(attrs \\ %{}) do
      # Dictをマージする キーが被っている時は第二引数のものが優先される
      changes = Dict.merge(%{
        name: "Some User",
        username: "user#{Base.encode16(:crypt.rand_bytes(8))}",
        password: "supersecret",
      }, attrs)
  
      %Rumbl.User{}
      |> Rumbl.User.registration_changeset(changes)
      |> Repo.insert!()
    end
  
    def insert_video(user, attrs \\ %{}) do
      user
      |> Ecto.build_assoc(:video, attrs)
      |> Repo.insert!()
    end
  end

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
