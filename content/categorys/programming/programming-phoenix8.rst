Programming Phoenix勉強その8
################################

:date: 2017-01-22 00:00
:tags: Elixir,Phoenix
:slug: programming-phoenix8
:related_posts: programming-phoenix7
:summary: Programming Phoenixって本を読むその8

| その8です。
| ここからchapter6です。 ``Ecto`` をコードジェネレータを色々探るみたいです。
|

===========================
コードジェネレータの利用
===========================

| 早速コードジェネレータを使ってみます。 ``rumbl`` ビデオにコメントを付けられるアプリなので ``Video`` 周りが色々と必要そうです。
| ``Video`` 周りのものはコードジェネレータにおまかせしてみます。以下のコマンドを入力します。
|

.. code-block:: shell
  :linenos:

  rumbl $ mix phoenix.gen.html Video videos user_id:references:users url:string title:string description:text

| モデル名の複数形とかモジュール名とかフィールドの型情報とかを与えてやっています。
| マイグレーションの前に下準備を行います。 
| 認証処理は共有で使いたいので ``user_controller.ex`` にあった ``authenticate/2`` 関数は ``auth.ex`` に外出して置きます。
|

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.Auth do
    import Phoenix.Controller
    alias Rumbl.Router.Helpers
    ...
    def authenticate_user(conn, _opts) do
      # Plugで追加したassignの呼び出しが可能かどうか
      if conn.assigns.current_user do
        conn
      else
        conn
        |> put_flash(:error, "You must be logged in to access that page")
        |> redirect(to: Helpers.page_path(conn, :index))
        |> halt()
      end
    end
  end

| ``web.ex`` に以下を追加して全コントローラーとルーターで上記の認証関数を使えるようにします。
| 

.. code-block:: Elixir
  :linenos:

  ...
  def controller do
    quote do
      use Phoenix.Controller

      alias Rumbl.Repo
      import Ecto
      import Ecto.Query

      import Rumbl.Router.Helpers
      import Rumbl.Gettext
      import Rumbl.Auth, only: [authenticate_user: 2] # 追加
    end
  end
  ...
  def router do
    quote do
      use Phoenix.Router

      import Rumbl.Auth, only: [authenticate_user: 2] # 追加
    end
  end

| 当然、 ``user_controller.ex`` の認証プラグも ``authenticate_user`` に変えておきます。
| ``router.ex`` に新しいスコープを追加します。
|

.. code-block:: Elixir
  :linenos:

  scope "/manage", Rumbl do
    pipe_through [:browser, :authenticate_user]

    resouces "/videos", VideoController
  end

| ここまで行ってマイグレーションを行います。
| 空白文字の扱いについては、 ``controller`` 内に ``scrub_param`` という ``Plug`` が定義されており、これによって自動で ``nil`` に変換されているらしいです。


