Programming Phoenix勉強その4
################################

:date: 2017-01-07 00:00
:tags: Elixir,Phoenix
:slug: programming-phoenix4
:related_posts: programming-phoenix3
:summary: Programming Phoenixって本を読むその4


| その4です。
| その3の続きです。
| ``:show`` アクションの実装からです.
|

=========================
:showアクションの実装
=========================

| ``:show`` アクションで各ユーザの詳細を表示できるようにします.
| まず ``Controler`` を実装します.
|

.. code-block:: Elixir
  :linenos:

  def show(conn, %{"id" => id}) do
    user = Repo.get(Rumbl.User, id)
    render conn, "show.html", user: user
  end

| 次に, ``web/templates/user/show.html.eex`` を以下の内容で実装します.
|

.. code-block:: ERB
  :linenos:

  <h1>Showing User</h1>
  <b><%= first_name(@user) %></b> (<%= @user.id %>)

| よく見ると ``<b>`` タグの部分が ``index.html.eex`` とかぶっているのがわかります.
|

templateの分離
=========================

| 各テンプレートで重複している部分を別テンプレートに分離します.
| ``web/templates/user/user.html.eex`` を以下の内容で実装します.
|

.. code-block:: ERB
  :linenos:

  <b><%= first_name(@user) %></b> (<%= @user.id %>)

| 共通部分をくくりだしたので,既存のテンプレートを編集します.
| ``web/templates/user/index.html.eex`` を以下の内容に変更します.
| ``<%= render "user.html", user: user %>`` の部分が変更点です.
|

.. code-block:: ERB
  :linenos:

  <h1>Listing Users</h1>
  
  <table class="table">
    <%= for user <- @users do %>
      <tr>
        <td><%= render "user.html", user: user %></td>
        <td><%= link "View", to: user_path(@conn, :show, user.id) %></td>
      </tr>
    <% end %>
  </table>

| ``web/templates/user/show.html.eex`` も同様に変更します.
|

.. code-block:: ERB
  :linenos:

  <h1>Showing User</h1>
  <%= render "user.html", user: @user %>

| ``view`` はモジュール, ``template`` は関数と捉えると良いみたいです.
| ``iex -S mix`` で以下のコマンドを入力すると何が起きているかなんとなくわかります.
| ``view`` の部分が ``:safe`` とリストの入れ子のタプルになってて一見わかりにくいですが,リストの部分は単なるタグの入れ子になってるみたいです.
| 素のタグ部分と, ``<%= %>`` とか ``<% %>`` の部分とでわけられてるみたいです.
|

.. code-block:: shell
  :linenos:
  
  iex(1)> user = Rumbl.Repo.get Rumbl.User, "1"
  %Rumbl.User{id: "1", name: "Jose", password: "elixir", username: "josevalim"}
  iex(2)> view = Rumbl.UserView.render("user.html", user: user)
  {:safe, [[[[["" | "<b>"] | "Jose"] | "</b> ("] | "1"] | ")\n"]}
  iex(3)> Phoenix.HTML.safe_to_string(view)
  "<b>Jose</b> (1)\n"

| ``:safe`` はこのHTMLが安全であることを示しています.
| また、リストになっているのはパフォーマスのためだそうです.
| ぱっと見どのテンプレートも ``render`` 関数呼び出しで呼び出されるっぽいですがテンプレート名でパターンマッチが行われることによってレンダリングしてるようです.
| この後 ``error`` の実装を行いますが,そっちを見るとよりわかりやすそうです.
|
