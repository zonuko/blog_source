Programming Phoenix勉強その20
################################

:date: 2017-02-15 23:52
:tags: Elixir,Phoenix
:slug: programming-phoenix20
:related_posts: programming-phoenix19
:summary: Programming Phoenixって本を読むその20

なんとその20です。 ``channel`` のテストの続きです。 ``wolfram`` のテストはしたので ``channel`` 周りのテストからです。

============================================
Channelのテスト
============================================

``wolfram`` のサービス用テストは作ったのでそれを呼び出す ``channel`` 側のテストを書きます。
まず認証をテストします。 ``rumbl/test/channel/user_socket_test.exs`` を実装します。


.. code-block:: Elixir
  :linenos:

  defmodule Rumbl.Channels.UserSocketTest do 
    use Rumbl.ChannelCase, async: true 
    alias Rumbl.UserSocket 
   
    test "socket authentication with valid token" do 
      token = Phoenix.Token.sign(@endpoint, "user socket", "123") 
   
      assert {:ok, socket} = connect(UserSocket, %{"token" => token}) 
      assert socket.assigns.user_id == "123" 
    end 
   
    test "socket authentication with invalid token" do 
      assert :error = connect(UserSocket, %{"token" => "123"}) 
      assert :error = connect(UserSocket, %{}) 
    end 
  end

単純にトークンを作った後にちゃんと処理ができるということを確かめているテストとトークン作らない場合に失敗するテストを書いています。
