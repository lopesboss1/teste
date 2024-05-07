'use strict';

//Import dependencias and set up http server
const 
    express = require('express'),
    bodyParser = require('body-parser'),
    crypto = require('crypto'),
    https = require('https'),
    request = require('request'),
    app = express().use(bodyParser.json()); //Create express http server

//Adding certificates LINK= https://sg.com.mx/revista/53/desarrollo-chatbots-para-facebook-messenger
var fs = require('fs');
/*
var options = {
    key : fs.redFileSync('/path/privKey.pem'),
    cert : fs.readFileSync('/path/cert.pem'),
    ca: fs.readFileSync
}
*/
//Set server port an logs message on success
app.listen(process.env.PORT || 4006, ()=> console.log('[INFO] webhook facebook listening'));
/***************************************************************************************************************************************/
/*                                                         HANDLES MESSAGES EVENTS                                                      /
/***************************************************************************************************************************************/
function handleMessage(sender_psid, received_message ) {
    let datetime = new Date();
    console.log("%s|INFO | handleMessage",datetime.toISOString());
    let response;
    //Check if the message contains text
    if(received_message.text) {
        //Create the payload for a basic text message
        response = {
            "text": received_message.text
        }
    }else if(received_message.attachments){
        //Get url of the message attachmednt
        let attachment_url = received_message.attachments[0].payload.url;
        response = {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "generic",
                "elements": [{
                  "title": "Is this the right picture?",
                  "subtitle": "Tap a button to answer.",
                  "image_url": attachment_url,
                  "buttons": [
                    {
                      "type": "postback",
                      "title": "Yes!",
                      "payload": "yes",
                    },
                    {
                      "type": "postback",
                      "title": "No!",
                      "payload": "no",
                    }
                  ],
                }]
              }
            }
          }
    } 
    //Sends the response message
    callSendAPI(sender_psid, response);
}
/***************************************************************************************************************************************/
function handlePostBack(sender_psid, received_postback) {
    let datetime = new Date();
    console.log("%s|INFO | shandlePostBack", datetime.toISOString());
    let response;
    // Get the payload for the postback
    let payload = received_postback.payload;
    // Set the response based on the postback payload
    if (payload === 'yes') {
      response = { "text": "Thanks!" }
    } else if (payload === 'no') {
      response = { "text": "Oops, try sending another image." }
    }
    // Send the message to acknowledge the postback
    callSendAPI(sender_psid, response);
}
/***************************************************************************************************************************************/
function callSendAPI(sender_psid, response) {
    let datetime = new Date();
    console.log("%s|callSenderAPI",datetime.toISOString());
    let request_body = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": sender_psid
        },
        "message": {
            "text": response
        }
    }
    console.log(request_body);
    // Send the HTTP request to the Messenger Platform "https://graph.facebook.com/v2.6/me/messages"
    request({
        "uri": "https://graph.facebook.com/v3.2/me/messages",
        "qs": { "access_token": "" },
        "method": "POST",
        "json": request_body
    }, (err, res, body) => {
        if (!err) {
            console.log('message sent!')
        } else {
            console.error("Unable to send message:" + err);
        }
    });
}
/***************************************************************************************************************************************/
app.post('/webhook', (req, res)=>{
    let datetime = new Date();
    let body = req.body;
    //Checks this is an event from a page subscription
    if (body.object == 'page') {
        //Iterates over each entry - there may be multiple if batched
        body.entry.forEach( function(entry){ //body.entry.array.forEach( function(entry){
            //Getting the message. entry.messaging is an array, but
            //will only contain one message, so we get index 0
            let webhook_event = entry.messaging[0];
            console.info("webhook_event = [%s]", webhook_event);
            //Get the sender PSID 
            let sender_psid = webhook_event.sender.id;
            console.info("%s|INFO | webhook_event| PSID:%s", datetime.toISOString(), sender_psid);
            //Chek if the event is a message or postback and pass the eventto aprropiate handler function
            if(webhook_event.message) {
                handleMessage(sender_psid, webhook_event.message);
            }else if(webhook_event.postback) {
                handlePostBack(sender_psid, webhook_event.postback);
            }

        });
        res.status(200).send('EVENT_RECEIVED');
    }else{
        console.warn("%s|ERROR| webhook_event|404| Event isn't from page subscription | %s |",datetime.toISOString(), body.object);
        res.sendStatus(404);
    }
});
/***************************************************************************************************************************************/
// Adds support for GET requests to our webhook
app.get('/webhook', (req, res) => {
    // Your verify token. Should be a random string.
    let VERIFY_TOKEN = "b7fac9153679d54790e630d804516238553b7a13"
    let datetime = new Date();
    // Parse the query params
    let mode = req.query['hub.mode'];
    let token = req.query['hub.verify_token'];
    let challenge = req.query['hub.challenge'];
      
    // Checks if a token and mode is in the query string of the request
    if (mode && token) {
    
      // Checks the mode and token sent is correct
      if (mode === 'subscribe' && token === VERIFY_TOKEN) {
        
        // Responds with the challenge token from the request
        console.log('%s|INFO| WEBHOOK_VERIFIED | mode=subscribe',datetime.toISOString());
        res.status(200).send(challenge);
      
      } else {
        // Responds with '403 Forbidden' if verify tokens do not match
        res.sendStatus(403);      
      }
    }
  });

//https://developers.facebook.com/docs/messenger-platform/getting-started/webhook-setup/?locale=es_ES

//Verificar server_fb
//curl -X GET "localhost:4006/webhook?hub.verify_token=b7fac9153679d54790e630d804516238553b7a13&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"

//Testing sending data
//curl -H "Content-Type: application/json" -X POST "localhost:1337/webhook" -d '{"object": "page", "entry": [{"messaging": [{"message": "TEST_MESSAGE"}]}]}'
