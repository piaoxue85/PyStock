import facebook

if __name__ == "__main__":

#https://developers.facebook.com/apps/576268022557717/dashboard/
  
  graph = facebook.GraphAPI('EAAIMHNrHrBUBAB4GCnOPMuC6vnUNgUdyaLdWTcJRvT28BdpRKKpTiuy6iZC9vx3tWNU3c17NiInB8rFMdtix9M9oBONh09FFRWS21bFw9RONscHpWNC3abNAH5CN88nQHAKouc42VQZBEoX5g26t5cWWbuplMJZB8bvzzLuMgZDZD')
  app_id = '576268022557717' # Obtained from https://developers.facebook.com/
  app_secret = '6fde634724cea221522b8a06baa49c4a' # Obtained from https://developers.facebook.com/

  # Extend the expiration time of a valid OAuth access token.
  extended_token = graph.extend_access_token(app_id, app_secret)

  print extended_token #verify that it expires in 60 days



  msg = "Everything is fine"
  status = graph.put_wall_post(msg)
  
  print "Everything is fine"
