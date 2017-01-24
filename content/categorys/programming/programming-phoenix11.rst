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
    @moduledoc """
    This module defines the test case to be used by
    tests that require setting up a connection.
  
    Such tests rely on `Phoenix.ConnTest` and also
    import other functionality to make it easier
    to build and query models.
  
    Finally, if the test case interacts with the database,
    it cannot be async. For this reason, every test runs
    inside a transaction which is reset at the beginning
    of the test unless the test case is marked as async.
    """
  
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
| 次の ``Ecto.Adapters.SQL.Sandbox.mode(Rumbl.Repo, {:shared, self()})`` は接続の共有方法を指定しているようです。非同期としてテストを行う場合は各テストケースで非同期にコネクションを使えるように明示しなくてならないようです。同期的にテストを行う場合はこちらのようです。（ ``allow/3`` 関数を使った非同期の方も書いてありましたが割愛します。）
| また、これは ``checkout`` された接続と同じ接続を使うようなので ``checkout`` の後に呼び出すのが必須なようです。
|
  
