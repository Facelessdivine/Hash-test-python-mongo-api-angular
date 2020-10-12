import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private URL = 'http://localhost:5000';

  selectUser: any;
  DatosUser: any[];


  constructor(private http: HttpClient, private router: Router) { }

  signUp(user){
    return this.http.post<any>(this.URL + '/signup', user);
  }
  signIn(user){
    return this.http.post<any>(this.URL + '/signin', user);
  }
  getUsers(){
    return this.http.get<any>(this.URL + '/users');
  }

  loggedIn(){
    return !!localStorage.getItem('token');
  }
  getToken(){
    return localStorage.getItem('token');

  }
  
  getTokenUser(){
    return JSON.parse(localStorage.getItem('token'));
  }

  logOut(){
    localStorage.removeItem('token');
    this.router.navigate(['/signin']);
  }
}
