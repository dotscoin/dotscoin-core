---
description: >-
  This page defines the commands provided by the rpc server in the dotscoin-core
  full node.
---

# RPC Commands



<table>
  <thead>
    <tr>
      <th style="text-align:left">Command</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Parameter</th>
      <th style="text-align:left">Body</th>
      <th style="text-align:left">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">addtransaction</td>
      <td style="text-align:left">This commands add transaction to the blockchain network for further verification.</td>
      <td
      style="text-align:left"></td>
        <td style="text-align:left">&lt;Transaction&gt;</td>
        <td style="text-align:left">
          <p>{</p>
          <p>&quot;status
            <br />&quot; : &lt;ok|failed&gt;</p>
          <p>}</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left">getlastblock</td>
      <td style="text-align:left">This command retrieves the last block from the blockchain.</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;block&quot;: &lt;Block&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getaddressbalance</td>
      <td style="text-align:left">This command retrieved the balance of the address by summing up all the
        UTXOs from the chain.</td>
      <td style="text-align:left">&lt;Address&gt;</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;balance&quot;: &lt;int&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getblockbyheight</td>
      <td style="text-align:left">This command returns the block specified by its height.</td>
      <td style="text-align:left">&lt;Height&gt;</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;block&quot;: &lt;Block&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">gettxbyhash</td>
      <td style="text-align:left">This command returns the transaction by hash</td>
      <td style="text-align:left">&lt;Hash&gt;</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;tx&quot;: &lt;Transaction&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getnodeinfo</td>
      <td style="text-align:left">This command returns the node address, enabled and disabled features.</td>
      <td
      style="text-align:left"></td>
        <td style="text-align:left"></td>
        <td style="text-align:left">
          <p>{</p>
          <p>&quot;address&quot;: &lt;string&gt;</p>
          <p>}</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left">getstakes</td>
      <td style="text-align:left">This command returns all the stakes done by the nodes for standing in
        the election.</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&lt;node_ip&gt;: &lt;stake_amount&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">gettxsbyaddress</td>
      <td style="text-align:left">This command returns all the transactions performed by the address.</td>
      <td
      style="text-align:left">&lt;Address&gt;</td>
        <td style="text-align:left"></td>
        <td style="text-align:left">
          <p>{</p>
          <p>&quot;txs&quot;: Array&lt;Transaction&gt;</p>
          <p>}</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left">getallutxobyaddress</td>
      <td style="text-align:left">This command returns all the UTXO(Unspent Transaction Output) by address.</td>
      <td
      style="text-align:left">&lt;Address&gt;</td>
        <td style="text-align:left"></td>
        <td style="text-align:left">
          <p>{</p>
          <p>&quot;utxos&quot;: Array&lt;{</p>
          <p>&quot;tx&quot;: &lt;hash&gt;,</p>
          <p>&quot;index&quot;: &lt;int&gt;</p>
          <p>}&gt;</p>
          <p>}</p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left">ping</td>
      <td style="text-align:left">This command checks the server health</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;reply&quot;: &quot;pong&quot;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getchainlength</td>
      <td style="text-align:left">This returns the total chain length</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;length&quot;: &lt;int&gt;</p>
        <p>}</p>
      </td>
    </tr>
  </tbody>
</table>

## JSON Data Format

```javascript
{
    "command": "string",
    "parameters": "string, string",
    "body": "string" // e.g. addtransaction body will be transaction
}
```



