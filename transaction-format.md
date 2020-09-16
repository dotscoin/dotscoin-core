---
description: This page specified the format used by the transaction.
---

# Transaction Format

Send transaction to any of node using the `addtransaction` RPC Command using the below defined format.

```typescript
interface TransactionInput {
    previous_tx: string;
    index: int;
    address: string;
    scriptSig: Array<string>;
    verifying_key: Array<string>;
}
```

```typescript
interface TransactionOutput {
    value: int;
    address: string;
    n: int;
}
```

```typescript
class Transaction {
    timestamp: float;
    version: string = "0.0.1";
    hash: string = "";
    inputs: Array<TransactionInput> = [];
    outputs: Array<TransactionOutput> = [];
    block = "";
}
```

