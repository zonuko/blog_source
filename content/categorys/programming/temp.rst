
// ここから先会社でやったもの。家出のものをプッシュし忘れていた。
============================================
InfoSysアプリの組み込み
============================================

準備が整ったので ``InfoSys`` を ``Rumbl`` に組み込みます。
今まで作った ``OTP`` アプリを ``VideoChannel`` に組み込みます。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.VideoChannel do
    ...
    # クライアントから直接送信された時に受け取るコールバック
    def handle_in("new_annotation", params, user, socket) do
      changeset =
        user
        |> build_assoc(:annotations, video_id: socket.assigns.video_id)
        |> Rumbl.Annotation.changeset(params)
  
      case Repo.insert(changeset) do
        {:ok, ann} ->
          # コメントを取り敢えず保存
          broadcast_annotation(socket, ann)
          # コメントに対するInfoSysの結果を取得する(非同期)
          # 取得結果はwolframユーザのannotationとして保存される
          Task.start_link(fn -> compute_additional_info(ann, socket) end)
          {:reply, :ok, socket}
        {:error, changeset} ->
          {:reply, {:error, %{errors: changeset}}, socket}
      end
    end
  
    defp compute_additional_info(ann, socket) do
      # computeには結果をスコア順で先頭一つだけ取るように指示
      # googleとかの結果もほしいならlimit2とかにすれば良いはず 
      # 結果は要らないのでリスト内包表記の結果は呼び出し元でも受け取っていない
      for result <- Rumbl.InfoSys.compute(ann.body, limit: 1, timeout: 10_000) do
        attrs = %{url: result.url, body: result.text, at: ann.at}
  
        info_changeset = 
          Repo.get_by!(Rumbl.User, username: result.backend) # ユーザを取得
          |> build_assoc(:annotations, video_id: ann.video_id) # ユーザに紐づくannotationを作成
          |> Rumbl.Annotation.changeset(attrs) # annotationのchangesetを作成
  
        case Repo.insert(info_changeset) do
          # インサート出来たらInfoSysの結果を共通関数でブロードキャストする
          {:ok, info_ann} -> broadcast_annotation(socket, info_ann)
          {:error, _changeset} -> :ignore
        end
      end
    end
    
    defp broadcast_annotation(socket, annotation) do
      annotation = Repo.preload(annotation, :user)
      rendered_ann = Phoenix.View.render(AnnotationView, "annotation.json", %{
        annotation: annotation
      })
      broadcast! socket, "new_annotation", rendered_ann
    end
  end

ほとんどコメントのままですが、 ``Task.start_link`` を使って他の処理をブロッキングしないように、
``InfoSys.compute`` を呼び出しています。
``compute_additional_info`` を見てもらうとわかるように ``result.backend`` がユーザとして存在することが
前提となっているので ``seed`` で追加します。

``backend_seeds.exs`` を以下のように実装します。

.. code-block:: Elixir
  :linenos:

  alias Rumbl.Repo
  alias Rumbl.User
  
  Repo.insert!(%User{name: "Wolfram", username: "wolfram"})

これでいつものようにスクリプトを実行すれば組み込みは完成です。
