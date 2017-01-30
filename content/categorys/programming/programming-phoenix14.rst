Programming Phoenix勉強その14
################################

:date: 2017-02-01 18:00
:tags: Elixir,Phoenix
:slug: programming-phoenix14
:related_posts: programming-phoenix13
:summary: Programming Phoenixって本を読むその14

その14です。その13の続きです。追加した ``Slug`` をURLに使ってアクセスできるようにします。

============================================
URLのカスタマイズ
============================================

URLを単なるID指定から ``id`` + 先程作成した ``slug`` でアクセスできるようにします。

``Phoenix.Param`` を ``impl`` することでカスタマイズ可能です。

.. code-block:: Elixir
  :linenos:

  defimpl Phoenix.Param, for: Rumbl.Video do
    def to_param(%{slug: slug, id: id}) do
      "#{id}-#{slug}"
    end
  end

`公式ドキュメント <https://hexdocs.pm/phoenix/Phoenix.Param.html>`_ を見ると単なる ``impl`` なら ``@derive {Phoenix.Param, key: :username}`` で行けるようです。
今回は ``"#{id}-#{slug}"`` などのちょっとカスタムされたURLでアクセスしたいので直接実装してます。（ ``derive`` で実装できる方法はあるのだろうか・・・）

``IEX`` で上記で作成したものを試してみます。

.. code-block:: shell
  :linenos:

  iex> video = %Rumbl.Video{id: 1, slug: "hello"}
  iex> Rumbl.Router.Helpers.watch_path(%URI{}, :show, video)
  "/watch/1-hello"

``watch_path/3`` の第一引数が ``%URI{}`` となっています。すべてのヘルパーはこのURI構造体を第一引数を取るらしいです。

URI構造体を使ってちょっと遊んでみます。

.. code-block:: shell
  :linenos:

  iex> url = URI.parse("http://example.com/prefix")
  %URI{authority: "example.com", fragment: nil, host: "example.com",
   path: "/prefix", port: 80, query: nil, scheme: "http", userinfo: nil}
  iex(6)> Rumbl.Router.Helpers.watch_url(url, :show, video)
  "http://example.com/prefix/watch/1-hello"

第一引数に与えたURLに続くパスとしてパスを構築してくれていることがわかります。じゃあ今使っている ``localhost`` のURLはどうなってんだという疑問がわきます。
以下を試してみます。

.. code-block:: shell
  :linenos:
  iex> url = Rumbl.Endpoint.struct_url
  %URI{authority: nil, fragment: nil, host: "localhost", path: nil, port: 4000,
   query: nil, scheme: "http", userinfo: nil}
  iex(8)> Rumbl.Router.Helpers.watch_url(url, :show, video)
  "http://localhost:4000/watch/1-hello"

どうやら内部的には ``struct_url`` で全体のURLが構築されているらしいことがわかります。また、 ``url`` というAPIもあるようです。
こちらは文字列でURL全体を返してくれます。

ここまでやって、ウォッチページにとぼうとするとエラーになります。 ``watch_controller`` の ``:show`` アクションではURLパラメータとして
``:id`` を期待しているのに ``1-hello`` のようなパラメータが来ているためです。これからこの点を修正します。
