import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class Private_taks_service {

  private URL = 'http://localhost:5000';

  selectUser: any;
  DatosUser: any[];


  constructor(private http: HttpClient, private router: Router) { }
    
  Update(user){
        return this.http.put<any>(this.URL + `/users/${user.id}`, user);
    }
  DeleteUser(user){
        return this.http.delete<any>(this.URL + `/users/${user}`, user);
    }
}
