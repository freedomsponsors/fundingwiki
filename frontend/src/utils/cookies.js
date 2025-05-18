import Cookies from 'js-cookie';
import {generateRandomString} from './string.js'

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      if (cookie.trim().startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.trim().slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function setUserCookie(){
  if(!Cookies.get('user_identify')){
    Cookies.set('user_identify', generateRandomString(20), { expires: 365 }); // expires in 365 days
  }
}