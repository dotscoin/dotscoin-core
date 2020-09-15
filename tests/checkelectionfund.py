        # print(self.redis_client.hget('fund '+self.fund_addr, "test234"))
        # # print(self.redis_client.hmset('fund '+self.fund_addr, {"test2": self.redis_client.hget('fund '+self.fund_addr,"test2") + 2}))
        # if self.redis_client.hget('fund '+self.fund_addr, "test234") == None:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": 2})
        # else:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": self.redis_client.hincrby('fund '+self.fund_addr, "test234", 3463)})

        # print(self.redis_client.hget('fund '+self.fund_addr, "test23"))

            # def run_election(self):
    #     self.get_stakes()
    #     self.vote_to()
    #     self.get_vote()
    #     dels = self.delegates()

    #     for dele in dels:
    #         if dele == self.this_node_addr:
    #             blk = Block()
    #             for i in range(0,20):
    #                 tx = self.redis_client.lindex('mempool', i).decode('utf-8')
    #                 if tx == None:
    #                     break
    #                 verify_verdict = self.verification.verify_tx(tx)
    #                 if verify_verdict == "verified":
    #                     #map to blk/create block
    #                     blk.add_transaction(tx)
    #                 else:
    #                     i =  i - 1
    #                     continue
    #             #add block
    #             blkChain = blockchain()
    #             blkChain.add_block(blk)

    #             #full blockchain verify
    #             full_verify_message = self.verification.full_chain_verify()
    #             if full_verify_message == "verified": 
    #                 pass
    #             else:
    #                 return