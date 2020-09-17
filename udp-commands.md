---
description: >-
  This command represents the protocol implemented by the nodes to communicate
  with each other for the purpose of consensus.
---

# UDP Commands



<table>
  <thead>
    <tr>
      <th style="text-align:left">Command</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">castvote</td>
      <td style="text-align:left">This command send vote to other nodes.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;node_addr&quot;: &lt;string&gt;,</p>
        <p>&quot;representative&quot;: &lt;string&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getchainlength</td>
      <td style="text-align:left">Get the total block chain length.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">getblockbyheight</td>
      <td style="text-align:left">This returns the block according to its height.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;height&quot;: &lt;int&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getmempoollength</td>
      <td style="text-align:left">This returns the total transactions inside the mempool.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">gettxbymindex</td>
      <td style="text-align:left">This returns the transaction by index inside the mempool.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;index&quot;: &lt;int&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">sendtransaction</td>
      <td style="text-align:left">This sends the transaction to the node.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;tx&quot;: &lt;Transaction&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">sendblock</td>
      <td style="text-align:left">This command send the block after being mined by a node.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;block&quot;: &lt;Block&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">getallmtxhash</td>
      <td style="text-align:left">This command returns the list of the transaction hashes in the mempool.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">gettxbyhash</td>
      <td style="text-align:left">This returns the transaction by its hash. (First it searches in the mempool
        and after that in the chain)</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;hash&quot;: &lt;string&gt;</p>
        <p>}</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">ping</td>
      <td style="text-align:left">This command checks the server UDP health.</td>
      <td style="text-align:left">
        <p>{</p>
        <p>&quot;reply&quot;: &quot;pong&quot;</p>
        <p>}</p>
      </td>
    </tr>
  </tbody>
</table>

## JSON UDP Data Format

```text
{
    "command": <string>,
    "body": <JSON Object>
}
```

## JSON UDP Response Format

```text
{
    "prev_command": <string>,
    "body": <JSON Object>
}
```

## 

