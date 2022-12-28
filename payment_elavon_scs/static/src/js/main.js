odoo.define('payment_elavon.payment_elavon',function(require){
    'use strict';
    var url = "https://api.demo.convergepay.com/hosted-payments/transaction_token"; // URL to Converge demo session token server
       var ajax = require('web.ajax');
        $(document).ready(function(){
        ajax.jsonRpc("/payment/get_env", 'call', {},{
        }).then(function(value){
                return ajax.loadJS(value);
        })

    $('#o_payment_form_pay').click(function(){

    ajax.jsonRpc("/payment/elavon_get_sale_order_detail", 'call', {"reference":$("input[name=reference]").val(),"order_id":$("input[name=order_id]").val(),"sale_order_id":$('.sale_order_id').val(),'inv_id':$('.inv_id').val()},{
        }).then(function(value){

           $.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: '/page/get_token',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'emp_id':{
                            ssl_transaction_type:'CCSALE',
                            ssl_first_name:value.fname,
                            ssl_last_name:value.lname,
                            ssl_get_token:'Y',
                            ssl_add_token:'Y',
                            ssl_amount:value.amount,
                            }}}),
                    success: function (data) {
                            var paymentFields = {
					        ssl_txn_auth_token: data['result']
			                         };
			                         			function showResult (status, msg) {

        }
                var callback = {
				onError: function (error) {
                if($("input[name='acquirer_name']").val()=='elavon'){


				    window.location.href ="/payment_fail?error=server_error";

				    }
				},
				onCancelled: function () {
				if($("input[name='acquirer_name']").val()=='elavon'){
						window.location.href ="/payment_fail?error=cancel";
						}
				},
				onDeclined: function (response) {
				if($("input[name='acquirer_name']").val()=='elavon'){
					window.location.href ="/payment_fail?error=declined";
					}
				},
				onApproval: function (response) {
				if($("input[name='acquirer_name']").val()=='elavon'){
                       	var jsondata = {
				                    'sale_order_id':value.id,
                                    'acquirer_id': $("input[name='acquirer_unique_id']").val(),
                                    'amount': $("input[name='ssl_amount']").val(),
                                    'reference': $("input[name='ssl_invoice_number']").val(),
                                    'order_no': $("input[name='ssl_invoice_number']").val(),
                                    'first_name': $("input[name='first_name']").val(),
                                    'last_name': $("input[name='last_name']").val(),
                                    'phone': $("input[name='phone']").val(),
                                    'email': $("input[name='email']").val(),
                                    'ssl_result_message':'APPROVED',
                                    'acquirer_reference':data.result
                                };

                                  ajax.jsonRpc("/payment/elavon/create_charge", 'call', jsondata,{
        }).then(function(){
            if ($.blockUI) {
                $.unblockUI();
            }
        }).then(function(data){
        window.location.href ="/payment/process";
        })

				}}
			};
			PayWithConverge.open(paymentFields, callback);
                    },
                    error: function(err){

                    }
                });
        })
    })
        })
   })