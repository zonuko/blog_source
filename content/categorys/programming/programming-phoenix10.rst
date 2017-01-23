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

より柔軟に ``Query`` を使いたい場合は ``fragments`` を使うことが出来る。

.. code-block:: Elixir
  :linenos:

  from(u in User, where: fragment("lower(username) = ?", ^String.downcase(uname)))

よくある静的プレースホルダと同じでしょうか。この方法でもセキュリティは担保されています。

もっと柔軟にクエリを投げたいときは以下のように直接SQLを実行できます。

.. code-block:: shell
  :linenos:

  iex> Ecto.Adapters.SQL.query(Rumbl.Repo, "SELECT power($1, $2)", [2, 10])

クエリで関連するものも取りたい時は以下

.. code-block:: shell
  :linenos:

  iex(6)> user = Repo.one from(u in User, limit: 1)
  [debug] QUERY OK source="users" db=16.0ms decode=15.0ms
  SELECT u0."id", u0."name", u0."username", u0."password_hash", u0."inserted_at", u0."updated_at" FROM "users" AS u0 LIMIT 1 []
  %Rumbl.User{__meta__: #Ecto.Schema.Metadata<:loaded, "users">, id: 1,
   inserted_at: ~N[2017-01-11 03:37:33.878000], name: "aaa", password: nil,
   password_hash: "$2b$12$L2IGA8kAewNvbOLJ0/c7i.4m6k18hAmuTSG4JuaHhyUK0qWfB0hae",
   updated_at: ~N[2017-01-16 03:40:31.371000], username: "aaa",
   videos: #Ecto.Association.NotLoaded<association :videos is not loaded>}
  iex(7)> user.videos # この時点ではNotLoaded
  #Ecto.Association.NotLoaded<association :videos is not loaded>
  iex(8)> user = Repo.preload(user, :videos) # preloadすると関連するものも取れる
  [debug] QUERY OK source="videos" db=78.0ms
  SELECT v0."id", v0."url", v0."title", v0."description", v0."user_id", v0."category_id", v0."inserted_at", v0."updated_at", v0."user_id" FROM "videos" AS v0 WHERE (v0."user_id" = $1)
   ORDER BY v0."user_id" [1]
  %Rumbl.User{__meta__: #Ecto.Schema.Metadata<:loaded, "users">, id: 1,
   inserted_at: ~N[2017-01-11 03:37:33.878000], name: "aaa", password: nil,
   password_hash: "$2b$12$L2IGA8kAewNvbOLJ0/c7i.4m6k18hAmuTSG4JuaHhyUK0qWfB0hae",
   updated_at: ~N[2017-01-16 03:40:31.371000], username: "aaa", videos: []}
  iex(9)> user.videos
  []

``Repo.preload`` 関数を使えば関連するものも一緒に取得できます。ただ、毎回 ``user`` の取得と ``preload`` を別々にやるのは面倒なので以下のようなオプションが良いされてます。

.. code-block:: shell
  :linenos:

  iex(10)> user = Repo.one from(u in User, limit: 1, preload: [:videos])
  [debug] QUERY OK source="users" db=0.0ms
  SELECT u0."id", u0."name", u0."username", u0."password_hash", u0."inserted_at", u0."updated_at" FROM "users" AS u0 LIMIT 1 []
  [debug] QUERY OK source="videos" db=16.0ms
  SELECT v0."id", v0."url", v0."title", v0."description", v0."user_id", v0."category_id", v0."inserted_at", v0."updated_at", v0."user_id" FROM "videos" AS v0 WHERE (v0."user_id" = $1)
   ORDER BY v0."user_id" [1]
  %Rumbl.User{__meta__: #Ecto.Schema.Metadata<:loaded, "users">, id: 1,
   inserted_at: ~N[2017-01-11 03:37:33.878000], name: "aaa", password: nil,
   password_hash: "$2b$12$L2IGA8kAewNvbOLJ0/c7i.4m6k18hAmuTSG4JuaHhyUK0qWfB0hae",
   updated_at: ~N[2017-01-16 03:40:31.371000], username: "aaa", videos: []}
  iex(11)>

``join`` も普通に出来ます。

.. code-block:: shell
  :linenos:

  iex(11)> Repo.all from u in User,
  ...(11)>   join: v in assoc(u, :videos),
  ...(11)>   join: c in assoc(v, :category),
  ...(11)>   where: c.name == "Comedy",
  ...(11)>   select: {u, v}
  [debug] QUERY OK source="users" db=31.0ms
  SELECT u0."id", u0."name", u0."username", u0."password_hash", u0."inserted_at", u0."updated_at", v1."id", v1."url", v1."title", v1."description", v1."user_id", v1."category_id", v1.
  "inserted_at", v1."updated_at" FROM "users" AS u0 INNER JOIN "videos" AS v1 ON v1."user_id" = u0."id" INNER JOIN "categories" AS c2 ON c2."id" = v1."category_id" WHERE (c2."name" =
  'Comedy') []
  []
  iex(12)>
