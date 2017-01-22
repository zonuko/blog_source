Programming Phoenix勉強その10
################################

:date: 2017-01-24 22:21
:tags: Elixir,Phoenix
:slug: programming-phoenix10
:related_posts: programming-phoenix9
:summary: Programming Phoenixって本を読むその10

| その10です。
| chapter7の続きです。
|

============================
Ecto.Queryの利用
============================

| 前のChapterで調べた ``Ecto.Query`` を利用して ``Category`` にソート用の ``query`` と取得用の ``query`` を生成できる関数を用意します。
|

.. code-block:: Elixir
  :linenos:

  def alphabetical(query) do
    from c in query, order_by: c.name
  end

  def names_and_ids(query) do
    from c in query, select: {c.name, c.id}
  end

============================
テンプレートの準備
============================

| カテゴリ一覧は取得できるようになったのでそれを表示できるようにしておきます。
| ``video/form.html.eex`` を以下のように編集します。
|

.. code-block:: ERB
  :linenos:

  <%= form_for @changeset, @action, fn f -> %>
    ...
    <!-- 追加 -->
    <div class="form-group">
      <%= label f, :category_id, "Category", class: "control-label" %>
      <%= select f, :category_id, @categories, class: "form-control", prompt: "Choose a category" %>
    </div>
    ...
  <% end %>

| ``video/new.html.eex`` を以下のように編集します。
|

.. code-block:: ERB
  :linenos:

  <h2>New video</h2>
  
  <%= render "form.html", changeset: @changeset, categories: @categories,
                          action: video_path(@conn, :create) %>
  
  <%= link "Back", to: video_path(@conn, :index) %>

| ``video/edit.html.eex`` を以下のように編集します。
|

.. code-block:: ERB
  :linenos:

  <h2>Edit video</h2>
  
  <%= render "form.html", changeset: @changeset, categories: @categories,
                          action: video_path(@conn, :update, @video) %>
  
  <%= link "Back", to: video_path(@conn, :index) %>

|

============================
QueryのAPIについて
============================

| ``Query`` 構築の際に使えるものは以下

- ``==, !=, <=, >=,<,>``
- ``and, or, not``
- ``in``
- ``like,ilike``
- ``is_nil``
- ``count, avg, sum, min, max``
- ``datetime_add, date_add``
- ``fragment, field, type``
