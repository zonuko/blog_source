Programming Phoenix勉強その19
################################

:date: 2017-02-12 23:52
:tags: Elixir,Phoenix
:slug: programming-phoenix19
:related_posts: programming-phoenix18
:summary: Programming Phoenixって本を読むその19

その19です。ここからChapter12です。今まで作った ``InfoSys`` アプリとかを
アンブレラプロジェクトに変更してテストしやすくするみたいです。

============================================
rumbrellaプロジェクトの作成と設定
============================================

以下のコマンドでアンブレラプロジェクトを新たに生成します。
既存の ``rumbl`` プロジェクトと混じらないように適当な場所で実行します。

.. code-block:: shell
  :linenos:

  $ mix new rumbrella --umbrella

アンブレラプロジェクトが作成されたので、 ``cd rumbrella/app`` に移動して以下のコマンドを実行します。

.. code-block:: shell
  :linenos:

  app $ mix new info_sys

準備が出来たので既存の ``Rumbl.InfoSys`` と ``Rumbl`` を ``rumbrella`` 管理下に移植していきます。
まず ``Rumbl.InfoSys`` からやっていきます。以下の流れです。

#. ``Rumbl.InfoSys`` のモジュール名を ``InfoSys`` に変更して、 ``lib/rumbl/info_sys.ex`` を ``app`` フォルダで作成した ``info_sys/lib/info_sys.ex`` となるように移動します。
#. ``Rumbl.InfoSys.Supervisor`` も同じようにリネームして ``info_sys/lib/info_sys/supervisor.ex`` となるように移動します。
#. ``Rumbl.InfoSys.Wolfram`` も ``supervisor`` と同じようにして同じフォルダに移動します。
#. ``Rumbl.InfoSys`` となっている箇所をすべて ``InfoSys`` に置換します。
#. ``Wolfram Alpha`` のAPIキーを取得する関数を以下のように変更します。

.. code-block:: Elixir
  :linenos:

  defp app_id, do: Application.get_env(:info_sys, :wolfram)[:app_id]

6. 依存関係を移し替えておきます。 ``info_sys`` の ``mix.exs`` の ``deps`` に ``{:sweet_xml, "~> 0.5.0"}`` を追加します。

これで ``InfoSys`` の移動は完了です。以下を実行しておきます。

.. code-block:: shell
  :linenos:

  rumbrella $ mix deps.get
  rumbrella $ mix test

次は ``Rumbl`` 本体の移植を行います。

============================================
Rumblプロジェクトのrumbrellaへの移植
============================================

``Rumbl`` プロジェクトを ``rumbrella`` に移植します。


#. ``rumbl`` ディレクトリを ``rumbrella/apps`` 以下に移動します。
#. ``rumbl`` の ``mix.exs`` 内の ``project`` 関数に ``info_sys`` の ``mix.exs`` と合わせるような感じで以下を追加します。

.. code-block:: Elixir
  :linenos:

  def project do
    [app: :rumbl,
     version: "0.0.1",
     elixir: "~> 1.2",
     elixirc_paths: elixirc_paths(Mix.env),
     compilers: [:phoenix, :gettext] ++ Mix.compilers,
     build_embedded: Mix.env == :prod,
     start_permanent: Mix.env == :prod,
     aliases: aliases(),
     build_path: "../../_build",
     config_path: "../../config/config.exs",
     deps_path: "../../deps",
     lockfile: "../../mix.lock",
     deps: deps()]
  end

3. ``mix.exs`` の ``application`` 関数に ``:info_sys`` を追加します。 ``:comeonin`` の後に追加する感じです。
#. ``deps`` の ``:sweet_xml`` を削除して ``{:info_sys, in_umbrella: true}`` を追加します。
#. ``lib/rumbl.ex`` から ``children`` として追加していた ``Rumbl.InfoSys`` を削除します。
#. ``video_channel.ex`` で使っていた ``Rumbl.InfoSys`` を ``InfoSys`` に変更します。
#. ``dev.secret.exs`` の ``WolframAlpha`` のキー部分を ``:rumbl`` から ``:info_sys`` に変更します。

これで準備OKです。

最後に ``mix deps.get`` と ``mix test`` を実行しておきます。

============================================
OTPのテスト
============================================

ここで終わると短いので、このまま ``chapter13`` に入って ``OTP`` のテストを行います。
