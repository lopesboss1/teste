var express = require('express');
var bodyparser = require('body-parser')
var app = express().use(bodyparser.json()) //http server
var port = 3009

app.get('/', (req,res) => {
    console.log("[INFO] Event GET")
    console.log("Printing request")
    console.log(req.query)
    console.log("Printing response")
    console.log(res.query)
    res.status(200).send('OK')
})

app.post('/', (req,res) => {
    console.log("[INFO] Event POST")
    console.log("Printing request")
    console.log(req.query)
    console.log("Printing response")
    console.log(res.query)
    res.status(200).send('OK')
})


app.listen(port, () => console.log('[INFO] Listening to elasticsearch on port 3200.'));
