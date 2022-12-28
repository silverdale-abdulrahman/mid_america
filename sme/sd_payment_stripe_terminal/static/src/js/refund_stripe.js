odoo.define('sd_payment_stripe_terminal.test_widget', function (require) {
    "use strict";

    var FieldChar = require('web.basic_fields').FieldBoolean;
    var ajax = require("web.ajax");
    var acquirerID;
    var terminal;



    function connectReaderHandler(is_test, location_id) {
    if (is_test) {
      // for simulator reader
      var config = { simulated: true };
    } else {
      // for card reader

      var config = { simulated: false, location: location_id };
    }

    var data;
    return terminal.discoverReaders(config).then(function (discoverResult) {
      if (discoverResult.error) {
        console.log("Failed to discover: ", discoverResult.error);
        data = {
          error: true,
          message: discoverResult.error.message,
        };
        return data;
      } else if (discoverResult.discoveredReaders.length === 0) {
        console.log(
          "No available readers.Please check your reader is registered with your stripe location or not!"
        );
        data = {
          error: true,
          message:
            "No available readers.Please check your reader is registered with your stripe location or not! ",
        };
        return data;
      } else {
        // Just select the first reader here.
        var selectedReader = discoverResult.discoveredReaders[0];

        return terminal
          .connectReader(selectedReader, { fail_if_in_use: true })
          .then(function (connectResult) {
            if (connectResult.error) {
              console.log("Failed to connect: ", connectResult.error);
              var data = {
                error: true,
                message: connectResult.error.message,
              };
              return data;
            } else {
              console.log("Connected to reader: ", connectResult.reader.label);
              var data = {
                error: false,
                message: connectResult.reader.label,
              };

              return data;

              //
            }
          });
      }
    });
  }

   function connection_stripe_terminal() {
   debugger
    return ajax
      .jsonRpc("/connection_token", "call", {
        acquirer_id: acquirerID,
      })
      .then(function (response) {
      debugger
        return JSON.parse(response);
      })
      .then(function (data) {
        if (data.error) {
          return data;
        } else return data.secret;
      });
  }
  function unexpectedDisconnect() {
    //    don't remove this fucntion. it is using to call stripe sdk
  }
    var CustomFieldChar = FieldChar.extend({
       events: _.extend({
    //            "keyup": "_onChange"
                  "input": "_onChange"
    //            "focus": "_onChange",
        }, FieldChar.events),
        _onChange: function(e) {
        console.log("onchange called here");




            var self = this

            if(self.record.data.line_ids.data[0].context.active_id){

            console.log("POS label calling ")
             self._super.apply(self, arguments)


              this._rpc({
                    model: 'account.payment.register',
                    method: 'refund_stripe',
                    args: [self.record.data.line_ids.data[0].context.active_id], //Now gives the value of c.
                }).then(function(res)
                {

                    console.log("POS label calling ",res)


                    if(res){


//                         self.do_action(res);
                        acquirerID = res.acq_id
                        var is_test = true
                        var location_id = true


                         terminal = StripeTerminal.create({
                            onFetchConnectionToken: connection_stripe_terminal,
                            onUnexpectedReaderDisconnect: unexpectedDisconnect,
                          });

                         connectReaderHandler(is_test, location_id).then(function(response)
                         {
                                       debugger
                                           terminal.collectRefundPaymentMethod(
                                                res.charge_id,
                                                100,
                                                "cad"
                                              ).then(function(response)
                                                        {
                                                        debugger;
                                                        if (response.error) {
                                                        // Placeholder for handling result.error
                                                      } else {
                                                        terminal.processRefund().then(function(refund)
                                                        {
                                                        debugger;
                                                          if (refund.error) {
                                                          // Placeholder for handling refund.error
                                                        } else {
                                                          console.log("Charge fully refunded!");
                                                          return refund;
                                                        }
                                                        })

                                                      }
                                                        })


                                        })


                    }


                });


             }

        },
    });


    var fieldRegistry = require('web.field_registry');

    fieldRegistry.add('test_widget', CustomFieldChar);
    });







