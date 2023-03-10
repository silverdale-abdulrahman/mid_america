odoo.define("sd_payment_stripe_terminal.payment_form", function (require) {
  "use strict";

  var ajax = require("web.ajax");
  var core = require("web.core");
  var PaymentForm = require("payment.payment_form");
  var rpc = require("web.rpc");

  var _t = core._t;
  var $modal;
  var $is_invoice;
  var $sale_order;
  var cust_payment;
  var terminal;
  var acquirerID;
  var simulate_card_response;
  var reader_connected = false;
  var time_interval;
  var download_url;
  var title = "Stripe terminal payment failed";
  //const { Gui } = require("point_of_sale.Gui");

  $(document).on("click", "#cancel_payment", function () {
    Promise.reject();

    console.log("Order ID !!!!!!!!!!!!", $("#order_id").val());
    var order_id = $("#order_id").val();
    var order_type = $("#order_type").val();
    var acquirerID = $("#acq_id").val();
    Promise.resolve();
     try {
      if (terminal && reader_connected) {

       terminal.cancelCollectPaymentMethod().then(function (config) {
          if (config) {
            var message = "Your payment request has been cancelled";

            console.log("Successfully Cancelled the payment. ", config);
            window.location.reload();
          } else {
            console.log("Failed to Cancel the payment. ");
              ajax
              .jsonRpc("/fail/payment", "call", {
                title: title,
                message: message,
                acquirer_id: acquirerID,
                order: order_id,
                order_type: order_type,

              })
              .then(function (response)
              {
              reader_connected = false
                window.location.reload();

              });
            //            return Promise.reject()
          }
        });



      } else {
        window.location.reload();
      }
    } catch (e) {
      window.location.reload();
    }


  });

  function connection_stripe_terminal() {
    return ajax
      .jsonRpc("/connection_token", "call", {
        acquirer_id: acquirerID,
      })
      .then(function (response) {
        return JSON.parse(response);
      })
      .then(function (data) {
        if (data.error) {
          return data;
        } else return data.secret;
      });
  }

  function capturePayment(
    payment_id,
    acquirerID,
    orderId,
    order_type,
    pay_status,
    interac_type,
    last_4_digit,
    card_holder,
    card_type,
    charge_id
  ) {
    // Your backend should call /v1/terminal/connection_tokens and return the JSON response from Stripe

    return ajax
      .jsonRpc("/capture_payment", "call", {
        payment_id: payment_id,
        acquirer_id: acquirerID,
        order: orderId,
        order_type: order_type,
        payment_status: pay_status,
        st_interac_present: interac_type,
        last_4_digit: last_4_digit,
        card_holder: card_holder,
        card_type: card_type,
        charge_id: charge_id,
      })
      .then(function (response) {
        return response;
      });
  }

  function unexpectedDisconnect() {
    //    don't remove this fucntion. it is using to call stripe sdk
  }

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

  PaymentForm.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Returns the parameters for the AcceptUI button that AcceptJS will use.
     *
     * @private
     * @param {Object} formData data obtained by getFormData
     * @returns {Object} params for the AcceptJS button
     */
    _acceptJsParams: function (formData) {
      return {
        class: "AcceptUI d-none",
        "data-apiLoginID": formData.login_id,
        "data-clientKey": formData.client_key,
        "data-billingAddressOptions": '{"show": false, "required": false}',
        "data-responseHandler": "responseHandler",
      };
    },

    _createPaymentMethod: function (stripe, formData, card, addPmEvent) {
      if (addPmEvent) {
        return this._rpc({
          route: "/payment/stripe/s2s/create_setup_intent",
          params: { acquirer_id: formData.acquirer_id },
        }).then(function (intent_secret) {
          return stripe.handleCardSetup(intent_secret, card);
        });
      } else {
        return stripe.createPaymentMethod({
          type: "card",
          card: card,
        });
      }
    },

    _createStripeTerminalToken: function (ev, $checkedRadio, addPmEvent) {
      var self = this;
      download_url = false;

      if (ev.type === "submit") {
        var button = $(ev.target).find('*[type="submit"]')[0];
      } else {
        var button = ev.target;
      }
      acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
      var acquirerForm = this.$("#o_payment_add_token_acq_" + acquirerID);
      console.log("acquirer id", acquirerID);
      var inputsForm = $("input", acquirerForm);
      var formData = self.getFormData(inputsForm);
      console.log("form Data", this.options);

      if (this.options.partnerId === undefined) {
        console.warn(
          "payment_form: unset partner_id when adding new token; things could go wrong"
        );
      }
      if (this.options.successUrl) {
        $is_invoice = this.options.successUrl;
      }

      var temp = 0;
      var loader =
        "<div class='stripe_terminal_payment_loder' style='display:none;height=500px'></div>";
      $(".o_payment_form").after(loader);
      var $payment_method = $("#payment_method");
      var $url_for_sale = $payment_method.find('input[name="prepare_tx_url"]');
      console.log("sale order", $url_for_sale);

      if ($url_for_sale[0]) {
        $sale_order = $url_for_sale[0].value;
      } else {
        $sale_order = this.options.orderId;
      }

      if (temp == 0) {
        var amount = $("#stripe_terminal-checkout")
          .find('input[name="amount"]')
          .val();
        temp = 1;

        $(".stripe_terminal_payment_loder").show();
        console.log("testing the logggggggggg");
        if (!$sale_order && !$is_invoice) {
          console.log("NO invoice and sale order founded...");
          cust_payment = window.location.href;
        }
        if (!$modal) {
          self = this;
          return rpc
            .query({
              model: "payment.acquirer",
              method: "action_is_key",
              args: [
                acquirerID,
                $sale_order,
                this.options.successUrl,
                cust_payment,
              ],
            })
            .then(function (result) {
              if (result.error == true) {
                //            self.unexpectedDisconnect();

                simulate_card_response = false;
                self._show_error(
                  result.message,
                  title,
                  acquirerID,
                  result.order,
                  result.order_type
                );

                return Promise.resolve();
              } else {
                //   var inv = this.options.successUrl

                $modal = $(result);
                $("#o_payment_form_pay").hide();
                console.log($(".modal-content").length);
                //                     $('.modal-body').css({"height":"550px"});
                if (!$is_invoice && $(".modal-content").length >= 1) {
                  console.log("Inside the invoice");
                  $(".modal-content").after($modal);
                } else {
                  console.log("#33333333333333333#####");
                  $(".o_payment_form").after($modal);
                  $("#o_payment_form_pay").after($modal);

                  //                   $('#o_payment_form_pay').after($modal);
                }
                $("#myModal").modal("show");
                $("#portal_pay").after($modal);
                self._sd_stripe_payment_terminal_pay(
                  acquirerID,
                  $sale_order,
                  $is_invoice,
                  cust_payment
                );
              }
            });
        }
        return false;
      }
    },

    _sd_stripe_payment_terminal_pay: function (
      acquirerID,
      sale_order,
      invoice,
      cust_payment
    ) {
      var self = this;

      return this.connection_stripe(
        acquirerID,
        sale_order,
        invoice,
        cust_payment,
        true
      ).then(function (data) {
        time_interval = data.time_interval;
        return self._sd_stripe_payment_terminal_handle_response(
          acquirerID,
          sale_order,
          invoice,
          cust_payment,
          data
        );
      });
    },

    //connection with stripe
    connection_stripe: function (
      acquirerID,
      sale_order,
      invoice,
      cust_payment,
      checks
    ) {
      return ajax
        .jsonRpc("/connection_token", "call", {
          orderId: $sale_order,
          invoice: this.options.successUrl,
          acquirer_id: acquirerID,
          link_url: cust_payment,
        })
        .then(function (response) {
          return JSON.parse(response);
        })
        .then(function (data) {
          if (data.error) {
            return data;
          } else {
            if (checks) {
              return data;
            } else {
              return data.secret;
            }
          }
        });
    },

    _poll_for_response: function (
      resolve,
      reject,
      is_test,
      acquirerID,
      amount,
      order_Id,
      order_type
    ) {
      var self = this;
      if (this.was_cancelled) {
        resolve(false);
        return Promise.resolve();
      }

      if (terminal) {
        if (is_test) {
          setTimeout(function () {
            terminal.setSimulatorConfiguration({
              testCardNumber: "4000001240000000",
            });
          }, 100);
        }

        var payment_intent = self._paymentIntent(
          acquirerID,
          amount,
          order_Id,
          order_type
        );
        var time_out;

        return payment_intent.then(function (data) {
          //            if there is error in response
          if (data.error) {
            if (self.remaining_polls != 0) {
              self.remaining_polls--;
              return Promise.reject();
              //              self._handle_odoo_connection_failure(data);
            } else {
              reject();
              self.poll_error_order = self.pos.get_order();
              return Promise.reject();
              //              self._handle_odoo_connection_failure(data);
            }
            resolve(false);
            return Promise.reject();
          } else {
            var clientSecret = data;
//            swipe card message
 rpc.query({
              model: "payment.acquirer",
              method: "waiting_template_message",
              args: [acquirerID, order_Id, order_type],
            })
            .then(function (result) {


                $modal = $(result);
                $("#o_payment_form_pay").hide();
                $("#myModal").hide();
                debugger;
                console.log($(".modal-content").length);

                if (!$is_invoice && $(".modal-content").length >= 1) {
                  console.log("Inside the invoice");
                  $(".modal-content").after($modal);
                } else {

                  $(".o_payment_form").after($modal);
                  $("#o_payment_form_pay").after($modal);
                  $("#myModal").after($modal);

                }
                $("#myModalCard").modal("show");
                debugger
                $("#portal_pay").after($modal);




              })
//             swipe card message
            return terminal
              .collectPaymentMethod(clientSecret)
              .then(function (result) {
                if (result.error) {
                  // Placeholder for handling result.error
                  console.log("Error while initiating payment", result.error);

                  if (self.remaining_polls != 0) {
                    self.remaining_polls--;
                    return Promise.reject();
                    //                    return self._handle_odoo_connection_failure(result);
                  } else {
                    self.poll_error_order = self.pos.get_order();
                    return Promise.reject();
                    //                    return self._handle_odoo_connection_failure(result);
                  }
                  return Promise.reject();
                } else {
                  // Placeholder for processing result.paymentIntent

                  console.log(
                    "Successfully initiated payment",
                    result.paymentIntent
                  );
                  clearTimeout(time_out);

                  //  self.remaining_polls = 2;
                  return terminal
                    .processPayment(result.paymentIntent)
                    .then(function (result) {
                      if (result.error) {
                        console.log(
                          "Error while Process payment",
                          result.error
                        );
                        var msg =
                          "Error while Process payment. " +
                          result.error.message;

                        self._show_error(
                          msg,
                          title,
                          acquirerID,
                          order_Id,
                          order_type
                        );

                        // Placeholder for handling result.error

                        if (self.remaining_polls != 0) {
                          self.remaining_polls--;
                        } else {
                          self.poll_error_order = self.pos.get_order();
                        }
                        return Promise.reject();
                      } else if (result.paymentIntent) {
                        // Placeholder for notifying your backend to capture result.paymentIntent.id
                        console.log(
                          "Successfully  payment",
                          result.paymentIntent.id
                        );

                        var interac_type;
                        var last_4_digit;
                        var card_holder;
                        var card_type;
                        var charge_id;
                        if (
                          result.paymentIntent.charges.data[0]
                            .payment_method_details.type == "interac_present"
                        ) {
                          interac_type =result.paymentIntent.charges.data[0].payment_method_details.type;
                          charge_id = result.paymentIntent.charges.data[0].id;
                          last_4_digit =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.interac_present.last4;
                          card_type =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.interac_present.brand;
                          card_holder =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.interac_present
                              .cardholder_name;
                        } else if (
                          result.paymentIntent.charges.data[0]
                            .payment_method_details.type == "card_present"
                        ) {
                          last_4_digit =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.card_present.last4;
                          charge_id = result.paymentIntent.charges.data[0].id;
                          card_type =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.card_present.brand;
                          card_holder =
                            result.paymentIntent.charges.data[0]
                              .payment_method_details.card_present
                              .cardholder_name;
                        }

                        return capturePayment(
                          result.paymentIntent.id,
                          acquirerID,
                          order_Id,
                          order_type,
                          result.paymentIntent.status,
                          interac_type,
                          last_4_digit,
                          card_holder,
                          card_type,
                          charge_id
                        ).then(function (response) {
                          if (response.error) {
                            var msg = response.error;

                            self._show_error(
                              msg,
                              title,
                              acquirerID,
                              order_Id,
                              order_type
                            );

                            resolve(false);
                            //                                                                                                        return Promise.reject(response)
                          } else {
                            resolve(true);
                            self.last_diagnosis_service_id = true;
                            if (response.download_url) {
                              var a = document.createElement("a");
                              a.href = response.download_url;
                              a.download = "download";

                              a.click();
                            }

                            console.log(
                              " self.last_diagnosis_service_id ",
                              self.last_diagnosis_service_id
                            );
                          }
                        });
                      }
                    });
                }
              });
          }

          if (self.remaining_polls <= 0) {
            var mesg =
              "The connection to your payment terminal failed. Please check if it is still connected to the internet.";

            self._show_error(mesg, title, acquirerID, order_Id, order_type);
            //            self._sd_stripe_payment_terminal_cancel();
            resolve(false);
          }
        });

        time_out = setTimeout(function () {
          self.remaining_polls = 4;
          clearInterval(self.polling);
          if (reader_connected) {
            var message = "Your payment request has been cancelled";
            ajax
              .jsonRpc("/fail/payment", "call", {
                title: title,
                message: message,
                acquirer_id: parseInt(acquirerID),
                order: parseInt(order_Id),
                order_type: order_type,
                cancel: true,
              })
              .then(function (response) {
                window.location.reload();
                terminal
                  .cancelCollectPaymentMethod()
                  .then(function (config) {});
              });
          } else {
            window.location.reload();
          }
        }, time_interval);
      }
    },

    _paymentIntent: function (acquirerID, amount, order_Id, order_type) {
      console.log("calling payment intent...");
      self = this;
      return ajax
        .jsonRpc("/payment_intent", "call", {
          acquirer_id: acquirerID,
          amount: amount,
          order_id: order_Id,
          order_type: order_type,
        })
        .then(function (response) {
          return response;
        })
        .then(function (data) {
          if (data.error) {
            var error = "Sorry! Could not Intent Payment. " + data.error;

            self._show_error(error, title, acquirerID, order_Id, order_type);
            console.log("Sorry! Could not Intent Payment. " + data.error);

            return Promise.reject();
            //              return data;
          } else {
            var clientSecret = data.client_secret;
            reader_connected = true;
            return clientSecret.toString();
          }
        });
    },

    _sd_stripe_payment_terminal_handle_response: function (
      acquirerID,
      sale_order,
      invoice,
      cust_payment,
      response
    ) {
      //            if (response.error) {
      if (!acquirerID) {
        var message =
          "Authentication failed. Please check your Stripe credentials.";

        this._show_error(message, title, acquirerID, sale_order, order_type);

        return Promise.resolve();
      } else {
        var self = this;

        var res = new Promise(function (resolve, reject) {
          // clear previous intervals just in case, otherwise
          // it'll run forever

          clearTimeout(self.polling);

          terminal = StripeTerminal.create({
            onFetchConnectionToken: connection_stripe_terminal,
            onUnexpectedReaderDisconnect: unexpectedDisconnect,
          });

          var is_test = false;
          var location_id;
          var device_name;
          var registration_code;
          var amount;
          var order_Id;
          var order_type;
          if (response && response.state && response.state == "test") {
            is_test = true;
          }
          if (response && response.location_id) {
            location_id = response.location_id;
          }

          if (response && response.amount) {
            amount = response.amount;
            order_Id = response.order_id;
            order_type = response.order_type;
          }

          simulate_card_response = connectReaderHandler(is_test, location_id);

          simulate_card_response.then(function (resp) {
            console.log("With Simulated card reader......", resp);
            debugger;
            self.polling = setInterval(function () {
              if (!resp.error) {
                if (resp && !resp.error) {
                  if (response.refund) {
                    terminal
                      .collectRefundPaymentMethod(
                        response.charge_id,
                         parseInt(response.amount*(100)),
                        response.currency
                      )
                      .then(function (ref_response) {
                        if (ref_response.error) {
                          Promise.reject();
                          self._show_error(
                            ref_response.error.message,
                            title,
                            acquirerID,
                            order_Id,
                            order_type
                          );
                        } else {
                          terminal.processRefund().then(function (refund) {
                            if (refund.error) {
                              Promise.reject();
                              self._show_error(
                                refund.error.message,
                                title,
                                acquirerID,
                                order_Id,
                                order_type
                              );
                            } else {
                             //
                                     rpc.query({
                            model: "account.payment.register",
                                    method: "create_refund_payment",
                                    args: [order_Id,acq_id],
                                        }).then(function (result) {
                                        console.log(result)
                                        resolve(true);
                                  self.last_diagnosis_service_id = true;
                                  if (response.download_url) {
                                    var a = document.createElement("a");
                                    a.href = response.download_url;
                                    a.download = "download";

                                    a.click();
                                  }
                                        });
                                    //
                              console.log("Charge fully refunded!");
//                              resolve(true);
//                                  self.last_diagnosis_service_id = true;
//                                  if (response.download_url) {
//                                    var a = document.createElement("a");
//                                    a.href = response.download_url;
//                                    a.download = "download";
//
//                                    a.click();
//                                  }

                            }
                          });
                        }
                      });
                  }
                  else {
                    var test = self._poll_for_response(resolve,reject,is_test,acquirerID,amount,order_Id,order_type);
                  }

                  if (self.last_diagnosis_service_id == true) {
                    clearTimeout(this.polling);
                  }

                  clearInterval(self.polling);

                  return test;
                } else {
                  var message;
                  if (resp && resp.message) {
                    if (resp.message.message) {
                      message = resp.message;
                    } else {
                      message = resp.message;
                    }
                  } else {
                    message =
                      "Failed to connect to the reader. Please retry again!";
                  }

                  console.log("Message", message);

                  self._show_error(
                    _t(message, title, acquirerID, order_Id, order_type)
                  );

                  resolve(false);
                }
              } else {
                var msg = resp.message;

                self._show_error(msg, title, acquirerID, order_Id, order_type);
                return Promise.reject();
              }
            }, 5500);
          });
        });

        // make sure to stop polling when we're done
        res.finally(function () {
          res.remaining_polls = 4;
          clearTimeout(res.polling);

          if (download_url) {
            window.location.href = download_url;

            window.location.reload();
          } else {
            window.location.reload();
          }

          //                    window.location = '/payment/process'
        });

        return res;
      }
    },
    /**
     * @override
     */
    updateNewPaymentDisplayStatus: function () {
      var $checkedRadio = this.$('input[type="radio"]:checked');

      if ($checkedRadio.length !== 1) {
        return;
      }

      //  hide add token form for stripe_terminal
      if (
        $checkedRadio.data("provider") === "stripe_terminal" &&
        this.isNewPaymentRadio($checkedRadio)
      ) {
        this.$('[id*="o_payment_add_token_acq_"]').addClass("d-none");
      } else {
        this._super.apply(this, arguments);
      }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    payEvent: function (ev) {
      ev.preventDefault();
      var $checkedRadio = this.$('input[type="radio"]:checked');
      console.log("$checkedRadio ", $checkedRadio.length);
      console.log("$checkedRadio.data", $checkedRadio.data("provider"));
      console.log(
        "$this.isNewPaymentRadio($checkedRadio)",
        this.isNewPaymentRadio($checkedRadio)
      );

      // first we check that the user has selected a stripe_terminal as s2s payment method
      if (
        $checkedRadio.length === 1 &&
        $checkedRadio.data("provider") === "stripe_terminal"
      ) {
        this._createStripeTerminalToken(ev, $checkedRadio);
        console.log("calling if ", ev);
      } else {
        this._super.apply(this, arguments);
        console.log("calling else ", ev);
      }
    },
    /**
     * @override
     */
    addPmEvent: function (ev) {
      ev.stopPropagation();
      ev.preventDefault();
      var $checkedRadio = this.$('input[type="radio"]:checked');
      console.log("check--------", $checkedRadio);

      // first we check that the user has selected a stripe_terminal as add payment method
      if (
        $checkedRadio.length === 1 &&
        this.isNewPaymentRadio($checkedRadio) &&
        $checkedRadio.data("provider") === "stripe_terminal"
      ) {
        this._createStripeTerminalToken(ev, $checkedRadio, true);
      } else {
        this._super.apply(this, arguments);
      }
    },

    _show_error: function (msg, title, acquirerID, orderId, order_type) {
      //    /fail/payment

      return ajax
        .jsonRpc("/fail/payment", "call", {
          title: title,
          message: msg,
          acquirer_id: acquirerID,
          order: orderId,
          order_type: order_type,
        })
        .then(function (response) {
          window.location.reload();
        });
    },

    create_draft_transaction: function (env) {
      var $payment_method = $("#payment_method");
      var $checked_radio = $payment_method.find('input[type="radio"]:checked');
      console.log("$checked_radio..........", $checked_radio.length);
      var acquirer_id = get_acquirer_id_from_radio($checked_radio);
      var $tx_url = $payment_method.find('input[name="prepare_tx_url"]');
      console.log("tx_url", $tx_url);

      if ($checked_radio.length === 1) {
        $checked_radio = $checked_radio[0];
        if ($tx_url.length === 1) {
          return ajax.jsonRpc($tx_url[0].value, "call", {
            acquirer_id: parseInt(acquirer_id),
          });
        } else {
          // we append the form to the body and send it.
          payment_display_error(
            _t("Cannot set-up the payment"),
            _t("We're unable to process your payment.")
          );
        }
      } else {
        payment_display_error(
          _t("No payment method selected"),
          _t("Please select a payment method.")
        );
      }
    },
  });
});
