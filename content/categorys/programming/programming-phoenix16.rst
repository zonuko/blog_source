Programming Phoenix勉強その16
################################

:date: 2017-02-09 00:18
:tags: Elixir,Phoenix
:slug: programming-phoenix16
:related_posts: programming-phoenix15
:summary: Programming Phoenixって本を読むその16

その16です。 ``Channel`` の続きからですが、コメント管理するモデルの作成からです。

============================================
モデルの作成
============================================

いつものコマンドからモデルを作成&マイグレーションします。

.. code-block:: shell
  :linenos:

  rumbl $ mix phoenix.gen.model Annotation annotations body:text as:integer user_id:references:users video_id:references:videos
  rumbl $ mix ecto.migrate

完了したら ``user.ex`` と ``video.ex`` に ``has_many :annotations, Rumbl.Annotation`` を追加しておきます。
作成したらモデルを使うようにしてやります。 ``video_channel.ex`` を以下のように変更します。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.VideoChannel do
    use Rumbl.Web, :channel
  
    def join("videos:" <> video_id, _params, socket) do
      {:ok, assign(socket, :video_id, String.to_integer(video_id))}
    end

    # 最初に入ってきてuserを取得後各関数に処理をディスパッチする
    def handle_in(event, params, socket) do
      user = Repo.get(Rumbl.User, socket.assigns.user_id)
      handle_in(event, params, user, socket)
    end
  
    def handle_in("new_annotation", params, user, socket) do
      changeset =
        user
        |> build_assoc(:annotations, video_id: socket.assigns.video_id)
        |> Rumbl.Annotation.changeset(params)
  
      case Repo.insert(changeset) do
        {:ok, annotation} ->
          # 接続しているクライアント全てにブロードキャストする
          # ユーザが任意のメッセージを送れないようにparamsを分解する
          broadcast! socket, "new_annotation", %{
            id: annotation.id,
            user: Rumbl.UserView.render("user.json", %{user: user}),
            body: annotation.body,
            at: annotation.at
          }
          {:reply, :ok, socket}
  
        {:error, changeset} ->
          {:reply, {:error, %{errors: changeset}}, socket}
      end
    end
  end

``handle_in/3`` 関数と ``handle_in/4`` 関数を追加しました。 ``user`` を必ず取得してから次の処理に移行するように
しています。

この中で ``UserVide.render`` 関数を使っているのでそちらも ``user_view.ex`` に実装します。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.UserView do
    use Rumbl.Web, :view
    alias Rumbl.User
  
    def first_name(%User{name: name}) do
      name
      |> String.split(" ")
      |> Enum.at(0)
    end
  
    def render("user.json", %{user: user}) do
      %{id: user.id, username: user.username}
    end
  end

``render`` 関数を追加しました。普通の ``render`` 関数は第一引数にテンプレート名を受けますが、
jsonを受けるようにして作りました。
