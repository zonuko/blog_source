Programming Phoenix勉強その18
################################

:date: 2017-02-09 22:18
:tags: Elixir,Phoenix
:slug: programming-phoenix18
:related_posts: programming-phoenix17
:summary: Programming Phoenixって本を読むその18

その18です。実際に ``OTP`` を使ったアプリを ``Rumbl`` に組み込みます。

============================================
InfoSysアプリの追加
============================================

``WolframAlpha`` のようなサービスを利用して動画の再生中に何かしらの質問をすると何か答えが返ってくるAPI
を追加します。

まず ``Supervisor`` を追加します。 ``lib/info_sys/supervisor.ex`` を実装します。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.InfoSys.Supervisor do
    use Supervisor
  
    def start_link() do
      Supervisor.start_link(__MODULE__, [], name: __MODULE__)
    end
  
    def init(_opts) do
      children = [
        worker(Rumbl.InfoSys, [], restart: :temporary)
      ]
      
      supervise children, strategy: :simple_one_for_one
    end
  end

今まで習ったとおりですが、戦略は ``:simple_one_for_one`` を使っています。

処理の本体が必要なので ``worker`` となる ``lib/info_sys.ex`` を実装します。これはバックエンドサービスが ``WolframAlpha`` 以外でも使えるように抽象化しておきます。

.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.InfoSys do
    # デフォルトのバックエンドサービス
    @backends [Rumbl.InfoSys.Wolfram]
  
    defmodule Result do
      defstruct score: 0, text: nil, url: nil, backend: nil
    end
  
    # バックエンドサービスのプロセスを開始する
    def start_link(backend, query, query_ref, owner, limit) do
      backend.start_link(query, query_ref, owner, limit)
    end
  
    def compute(query, opts \\ []) do
      limit = opts[:limit] || 10
      # 引数でバックエンドサービスが提示されてなければデフォルトを使う
      backends = opts[:backends] || @backends
  
      # 各バックエンドサービスに関してプロセスを開始する
      backends
      |> Enum.map(&spawn_query(&1, query, limit)
    end
  
    defp spawn_query(backend, query, limit) do
      query_ref = make_ref()
      opts = [backend, query, query_ref, self(), limit]
      # 起動済みのSupervisorに自分自身のプロセスを子として監視してもらう
      # これを呼び出すと自動でstart_linkが呼び出されてプロセス開始する
      {:ok, pid} = Supervisor.start_child(Rumbl.InfoSys.Supervisor, opts)
      {pid, query_ref}
    end
  end

モジュールのアトリビュート（ ``@backends`` ）でバックエンドサービスを管理しています。
``compute`` 関数を見てもらえればわかりますが、このアトリビュートに対して一つずつプロセスを起動しています。

戦略が ``:simple_one_for_one`` になっているので、子となるプロセスから ``Supervisor.start_child`` でプロセスを監視下に追加しています。

次に具体的なシステムを構築していきます。

============================================
Wolframを利用するアプリの構築
============================================

まず ``WolframAlpha`` を使うアプリを構築します。 ``mix.exs`` の ``deps`` に ``{:sweet_xml, "~> 0.5.0"},`` 
を追加して ``mix deps.get`` を実行しておきます。
この追加したモジュールはXMLのパーサーです。

また、 `ここから <https://www.wolframalpha.com/>`_ ``WolframAlpha`` のユーザ登録をしてAPIキーを取得します。ただし、当然ですがこのキーは ``dev.exs`` に直接書くのはNGです。
従って、 ``config/dev.secret.exs`` を用意して ``.gitignore`` に追加しておきます。
このファイルには ``WolframAlpha`` の設定を書いておきます。

.. code-block:: Elixir
  :linenos:

  use Mix.Config
  
  config :rumbl, :wolfram, app_id: "XXXXXX-XXXXXXXXXX"

最後に、元々の ``dev.exs`` に ``import_config "dev.secret.exs"`` を一行追加して準備完了です。
