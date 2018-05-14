#!/bin/bash
# echo 'xxxxxxxxxxx'
mongo --port 27020 <<EOF
rs.initiate( {
   _id : "rs0",
   members: [
      { _id: 0, host: "39.105.15.174:27020" },
      { _id: 1, host: "39.105.15.174:27021" },
      { _id: 2, host: "39.105.15.174:27021" }
   ]
})

