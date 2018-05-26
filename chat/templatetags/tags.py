from django import template
from Crypto.Cipher import AES
import secrets
register = template.Library()

key = secrets.token_urlsafe(16)[0:16]

@register.simple_tag
def enc_side(switch='encrypt'):
    encrypt = '''
                  var key = info.encrypt;
                  delete info.encrypt;
                  var sp = key.length % 2;
                  if(sp == 0){
                    sp = 2;
                  }
                  var total = 0;
                  for(var x=0;x<key.length;x++){
                    total += key.charCodeAt(x);
                  }
                  var forencrypt = info.message.split("");
                  var aftencrypt = [];
                  for (x of forencrypt){
                    if(sp==1){
                      aftencrypt.push(Math.floor(Math.random() * Math.floor(65556)))
                    } else {
                      aftencrypt.push(Math.floor(Math.random() * Math.floor(65556)))
                      aftencrypt.push(Math.floor(Math.random() * Math.floor(65556)))
                    }
                    aftencrypt.push(x.charCodeAt(0) + total)
                  }
                  info.message = aftencrypt;
                  socket.send(JSON.stringify(info));
                '''

    encrypt += ' ' * (16 - len(encrypt) % 16)

    if switch == 'encrypt':
        return list(AES.new(key, AES.MODE_CBC, 'This is an IV456').encrypt(encrypt))
    else:
        return key
