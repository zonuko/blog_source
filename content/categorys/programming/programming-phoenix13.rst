Programming Phoenix勉強その13
################################

:date: 2017-01-31 18:00
:tags: Elixir,Phoenix
:slug: programming-phoenix13
:related_posts: programming-phoenix12
:summary: Programming Phoenixって本を読むその13

その13です。ここからPart2です。ここから機能をちゃんと整備します。

- ビデオに対してリアルタイムコメントを付けられるように
- ビデオを再生可能に

をやっていくようです。はじめにビデオを再生可能にしていきます。


============================================
視聴用ページ作成
============================================

投稿されたビデオを見るためのページを作ります。いつものを作るのでソースのみ提示します。
``app.html.eex`` に投稿一覧表示用メニューを付けます。

.. code-block:: ERB
  :linenos:

  ...
  <body>
    <div class="container">
      <header class="header">
        <ol class="breadcrumb text-right">
          <!-- assignsで突っ込んだものが使えている -->
          <%= if @current_user do %>
            <li><%= @current_user.username %></li>
            <li><%= link "My Videos", to: video_path(@conn, :index) %></li>
            <li>
  ...

``watch_controller.ex`` を作成します。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.WatchController do
    use Rumbl.Web, :controller
    alias Rumbl.Video
  
    def show(conn, %{"id" => id}) do
      video = Repo.get!(Video, id)
      render conn, "show.html", video: video
    end
  end

``wathc/show.html.eex`` を作成します。コメント入力欄がある唯のページです。

.. code-block:: ERB
  :linenos:

  <h2><%= @video.title %></h2>
  <div class="row">
    <div class="col-sm-7">
      <%= content_tag :div, id: "video",
            data: [id: @video.id, player_id: player_id(@video)] do %>
      <% end %>
    </div>
    <div class="col-sm-5">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">Annotations</h3>
        </div>
        <div id="msg-container" class="panel-body annotations">
        </div>
        <div class="panel-footer">
          <textarea id="msg-input"
                    rows="3"
                    class="form-control"
                    placeholder="Comment...">
          </textarea>
          <button id="msg-submit" class="btn btn-primary form-control"
              type="submit">
            Post
          </button>
        </div>
      </div>
    </div>
  </div>

上記テンプレート内で ``player_id/1`` という関数を使っているので ``watch_view.ex`` を実装します。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.WatchView do
    use Rumbl.Web, :view
  
    def player_id(video) do
      ~r{^.*(?:youtu\.be/|\w+/|v=)(?<id>[^#&?]*)}
      |> Regex.named_captures(video.url)
      |> get_in(["id"])
    end
  end

正規表現を使って投稿されたYouTubeのURLに対してパラメータ部分のみを取り出しています。
``router.ex`` に ``/`` スコープに ``get "/watch/:id", WatchController, :show`` を追加しておきます。

最後に、ビデオ一覧画面にウォッチ画面へのリンクボタンを作成します。 ``video/index.html.eex`` に以下を追加します。

.. code-block:: ERB
  :linenos:

  ...
  <tbody>
    <%= for video <- @videos do %>
      <tr>
        <td><%= video.user_id %></td>
        <td><%= video.url %></td>
        <td><%= video.title %></td>
        <td><%= video.description %></td>

        <td class="text-right">
          <%= link "Watch", to: watch_path(@conn, :show, video), class: "btn btn-default btn-xs" %>
  ...

これで準備は完了です。次からJavaScript側のコードを作成します。

============================================
視聴用ページ作成
============================================

最初にPhoenixでのJavaScriptのビルド周りについて触れられています。

- ビルドツールは ``brunch`` がデフォルト
- ``brunch`` の設定はデフォルトでES6になっている
- ``web/static/js`` 以下にあるファイルをすべて ``app.js`` にまとめる
- staticファイルの読み込みは ``static_path(@conn, "/js/app.js")`` で行う
- モジュールシステムを利用しないライブラリは ``web/static/vendor`` に追加する

  - 公式ドキュメントによると ``bower`` で入れたものはこっちに配備されるっぽい？
