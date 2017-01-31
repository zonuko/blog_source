Programming Phoenix勉強その15
################################

:date: 2017-02-21 22:00
:tags: Elixir,Phoenix
:slug: programming-phoenix15
:related_posts: programming-phoenix14
:summary: Programming Phoenixって本を読むその15

その15です。ここからChapter10の ``Channel`` です。Phoenixの目玉機能の一つな気もするので楽しみです。

============================================
Channelについて
============================================

- ステートを持つ双方向通信である

  - ステートフルなので ``Cookie`` などを意識しなくて良い
- トピックと呼ばれる単位で各会話は管理される
- 各々の会話はプロセスで管理され、一つがバグっても他に影響を与えないし、並列性も持つ
- クライアント側はES6(ES2015)で記述する
- 実装するにあたりクライアントとサーバーで以下3つを意識する

  - 接続と切断
  - メッセージの送信
  - メッセージの受信

============================================
クライアントサイドの実装
============================================

というわけで、ES6でクライアントサイドから実装していきます。まず ``video.js`` を作成します。

.. code-block:: JavaScript
  :linenos:

  import Player from "./player"
  
  let Video = {
      init(socket, element) {
          if (!element) { return; }
          let playerId = element.getAttribute("data-player-id");
          let videoId = element.getAttribute("data-id");
          socket.connect()
          Player.init(element.id, playerId, () => {
              this.onReady(videoId, socket);
          });
      },
  
      onReady(videoId, socket) {
          let msgContainer = document.getElementById("msg-container");
          let msgInput = document.getElementById("msg-input");
          let postButton = document.getElementById("msg-submit");
          // トピックの識別
          let voidChannel = socket.channel("videos:" + videoId);
          // TODO: join the vidChannel
      }
  }
  export default Video;

``player`` の ``import`` をこっちに移設しています。また、 ``init`` メソッドと ``onReady`` メソッドを定義しています。
``onReady`` はコールバックとして使っているようです。
コメントにあるようにトピックの識別子は ``videoId`` としています。

``app.js`` を上の実装に合わせて変えておきます。 ``Player`` を作成していた部分に変わって ``Video`` の利用にします。

.. code-block:: JavaScript
  :linenos:

  import socket from "./socket";
  import Video from "./video";
  Video.init(socket, document.getElementById("video"));

デフォルトで用意されている ``socket.js`` のインポートも行っています。
このファイルについては後で触るようです。

通常のリクエストと ``socket`` のデータの流れの違いについても触れられています。
前の章で見たように通常のアクセスではデータは ``conn`` という形で各パイプラインを流れて、
その中で変換されていきます。 ``conn`` は新しい接続ごとに新しいものが作られて使われます。

一方 ``socket`` の方ではステートフルなためソケットの寿命まで一つの接続が変換され続けます。

============================================
socket.jsの変更
============================================

最初のソケットを作成します。 ``socket.js`` の中身を変更して実装していきます。

.. code-block:: JavaScript
  :linenos:

  import { Socket } from "phoenix"
  
  let socket = new Socket("/socket", {
      params: { token: window.userToken },
      // バッククオートで囲んだものがテンプレートリテラルとして値を文字に埋め込める
      logger: (kind, msg, data) => { console.log(`${kind}: ${msg}`, data); }
  });
  
  export default socket

余計な部分を消してしまって問題ないです。ログをコンソールに出すように変更しただけです。
