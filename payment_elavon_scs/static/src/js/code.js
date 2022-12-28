<html>

<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Checkout.js Demo</title>
    <script src="https://api.demo.convergepay.com/hosted-payments/Checkout.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
</head>

<body>
    <script>
        function initiateCheckoutJS() {
            var tokenRequest = {
                ssl_first_name: document.getElementById('name').value,
                ssl_last_name: document.getElementById('lastname').value,
                ssl_amount: document.getElementById('ssl_amount').value
            };
            $.post("checkoutjscurlrequestdevportal.php", tokenRequest, function (data) {
                document.getElementById('token').value = data;
                transactionToken = data;
            });
            return false;
        }

        function showResult(status, msg) {
            document.getElementById('txn_status').innerHTML = "<b>" + status + "</b>";
            document.getElementById('txn_response').innerHTML = msg;
        }
    </script>

    <script>
        function pay() {
            var token = document.getElementById('token').value;
            var card = document.getElementById('card').value;
            var exp = document.getElementById('exp').value;
            var cvv = document.getElementById('cvv').value;
            var gettoken = document.getElementById('gettoken').value;
            var addtoken = document.getElementById('addtoken').value;
            var firstname = document.getElementById('name').value;
            var lastname = document.getElementById('lastname').value;
            var merchanttxnid = document.getElementById('merchanttxnid').value;
            var paymentData = {
                ssl_txn_auth_token: token,
                ssl_card_number: card,
                ssl_exp_date: exp,
                ssl_get_token: gettoken,
                ssl_add_token: addtoken,
                ssl_first_name: firstname,
                ssl_last_name: lastname,
                ssl_cvv2cvc2: cvv,
                ssl_merchant_txn_id: merchanttxnid
            };
            var callback = {
                onError: function (error) {
                    showResult("error", error);
                },
                onDeclined: function (response) {
                    console.log("Result Message=" + response['ssl_result_message']);
                    showResult("declined", JSON.stringify(response));
                },
                onApproval: function (response) {
                    console.log("Approval Code=" + response['ssl_approval_code']);
                    showResult("approval", JSON.stringify(response));
                }
            };
            ConvergeEmbeddedPayment.pay(paymentData, callback);
            return false;
        }

        function showResult(status, msg) {
            document.getElementById('txn_status').innerHTML = "<b>" + status + "</b>";
            document.getElementById('txn_response').innerHTML = msg;
        }
    </script>

    </head>

    <body>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <form name="getSessionTokenForm">
            First Name: <input type="text" id="name" name="ssl_first_name" size="25" value="John"> <br><br>
            Last Name: <input type="text" id="lastname" name="ssl_last_name" size="25" value="Smith"> <br><br>
            Transaction Amount: <input type="text" id="ssl_amount" name="ssl_amount" value="25.00"> <br> <br>
            <button onclick="return initiateCheckoutJS();">Click to Confirm Order</button> <br>
        </form>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        Transaction Token: <input id="token" type="text" name="token"> <br />

        Card Number: <input id="card" type="text" name="card" value="4124939999999990" /> <br />
        Expiry Date: <input id="exp" type="text" name="exp" value="1219" /> <br />
        CVV2: <input id="cvv" type="text" name="cvv" value="123"> <br />
        Merchant TXN ID: <input id="merchanttxnid" type="text" name="merchanttxnid" value="MerchantTXNIDHere" /> <br />
        <input id="gettoken" type="hidden" name="gettoken" value="y" />
        <input id="addtoken" type="hidden" name="addtoken" value="y" />
        <button onclick="return pay();">Process Payment</button>

        </form>
        <br>
        <br>
        <br>
        <br>
        Transaction Status:<div id="txn_status"></div>
        <br>
        Transaction Response:<div id="txn_response"></div>

    </body>

</html>
Create a serverside script to safely handle the information collected from the form.

<?php

 // Set variables

$merchantID = "xxxxxx"; //Converge 6 or 7-Digit Account ID *Not the 10-Digit Elavon Merchant ID*
$merchantUserID = "convergeapi"; //Converge User ID *MUST FLAG AS HOSTED API USER IN CONVERGE UI*
$merchantPIN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"; //Converge PIN (64 CHAR A/N)

 $url = "https://api.demo.convergepay.com/hosted-payments/transaction_token"; // URL to Converge demo session token server
//$url = "https://api.convergepay.com/hosted-payments/transaction_token"; // URL to Converge production session token server

// Read the following querystring variables

$firstname=$_POST['ssl_first_name']; //Post first name
$lastname=$_POST['ssl_last_name']; //Post first name
$amount= $_POST['ssl_amount']; //Post Tran Amount

$ch = curl_init();    // initialize curl handle
curl_setopt($ch, CURLOPT_URL,$url); // set url to post to
curl_setopt($ch,CURLOPT_POST, true); // set POST method
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

// Set up the post fields. If you want to add custom fields, you would add them in Converge, and add the field name in the curlopt_postfields string.
curl_setopt($ch,CURLOPT_POSTFIELDS,
"ssl_merchant_id=$merchantID".
"&ssl_user_id=$merchantUserID".
"&ssl_pin=$merchantPIN".
"&ssl_transaction_type=ccsale".
"&ssl_first_name=$firstname".
"&ssl_last_name=$lastname".
"&ssl_get_token=Y".
"&ssl_add_token=Y".
"&ssl_amount=$amount"
);

curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_VERBOSE, true);

$result = curl_exec($ch); // run the curl procss
curl_close($ch); // Close cURL

echo $result;  //shows the session token.

 ?>
Sample Response
"ssl_card_number": "34**********1117", "ssl_transaction_type": "SALE", "ssl_result": "1", "ssl_txn_id": "031118MB-7E2DFD65-8317-45BD-A329-2501279FA0B5", "ssl_avs_response": " ", "ssl_approval_code": " ", "ssl_amount": "1.00", "cust_checkbox": "off", "ssl_txn_time": "11/03/2018 06:44:47 PM", "ssl_account_balance": "0.00", "ssl_exp_date": "1222", "ssl_result_message": "APPROVED", "ssl_card_short_description": "AMEX", "ssl_card_type": "CREDITCARD"
Sample Dynamic Currency Converter
This form includes the Dynamic Currency Conversion option for Checkout.js:

<!DOCTYPE HTML>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Embedded Payment DCC Demo</title>
    <script src="https://api.demo.convergepay.com/hosted-payments/EmbeddedPayment.min.js"></script>
    <script>

        var callback = {
            onError: function (error) {
                showResult("error", error);
            },
            onDeclined: function (response) {
                showResult("declined", JSON.stringify(response));
            },
            onApproval: function (response) {
                showResult("approval", JSON.stringify(response));
            },
            onDCCDecision: function (response) {
                document.getElementById('ssl_conversion_rate').value = response.ssl_conversion_rate;
                showResult("DCC decision", JSON.stringify(response));
            }
        };

        function showResult (status, msg) {
            document.getElementById('txn_status').innerHTML = "<b>" + status + "</b>";
            document.getElementById('txn_response').innerHTML = msg;
        }

        function pay () {
            var token = document.getElementById('token').value;
            var card = document.getElementById('card').value;
            var exp = document.getElementById('exp').value;
            var cvv = document.getElementById('cvv').value;
            var paymentData = {
                    ssl_txn_auth_token: token,
                    ssl_card_number: card,
                    ssl_exp_date: exp,
                    ssl_cvv2cvc2: cvv
            };
            ConvergeEmbeddedPayment.pay(paymentData, callback);
            return false;
        }

        function dcc (option) {
            ConvergeEmbeddedPayment.dccDecision(option, callback);
            return false;
        }
    </script>
  </head>
  <body>
        <form id="firstForm">
            Transaction Token: <input id="token" type="text" name="token"> <br/>
            Card Number: <input id="card" type="text" name="card" > <br/>
            Expiry Date: <input id="exp" type="text" name="exp" > <br/>
            CVV2: <input id="cvv" type="text" name="cvv"> <br/>
            <button onclick="return pay();">Pay</button>
        </form>
        <br>
            <form id="secondForm">
                Converion Rate: <input id="ssl_conversion_rate" type="text"> <br/>
                <button onclick="return dcc(true);">Pay with cardholder currency</button><br>
                <button onclick="return dcc(false);">Pay with transaction currency</button><br>
            </form>
        <br>
        Transaction Status:<div id="txn_status"></div>
        <br>
        Transaction Response:<div id="txn_response"></div>
  </body>
</html>
Sample 3D Secure Form
This form includes the 3D Secure function for Checkout.js:

<!DOCTYPE HTML>
<html>
<head>
    <script src="https://api.convergepay.com/hosted-payments/EmbeddedPayment.min.js"></script>
    <script>
    function threeDSecureReturn () {
        var md = document.getElementById('md').value;
        var pares = document.getElementById('pares').value;
        var callback = {
            onError: function (error) {
                showResult("error", error);
            },
            onDeclined: function (response) {
                showResult("declined", JSON.stringify(response));
            },
            onApproval: function (response) {
                showResult("approval", JSON.stringify(response));
            }
        };
        ConvergeEmbeddedPayment.threeDSecureReturn(md, pares, callback);
        return false;
    }
    function showResult (status, msg) {
        document.getElementById('txn_status').innerHTML = "<b>" + status + "</b>";
        document.getElementById('txn_response').innerHTML = msg;
    }
    </script>
</head>
<body>
    <form id="firstForm">
            PaRes: <input id="pares" type="text" name="pares"> <br/>
            MD: <input id="md" type="text" name="md"> <br/>
            <button onclick="return threeDSecureReturn();">Continue</button>
    </form>
    <br>
    Transaction Status:<div id="txn_status"></div>
    <br>
    Transaction Response:<div id="txn_response"></div>
</body>
</html>