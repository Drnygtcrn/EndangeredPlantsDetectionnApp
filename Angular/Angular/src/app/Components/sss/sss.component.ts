import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Sorular } from 'src/app/Classes/Sorular';


@Component({
  selector: 'app-sss',
  templateUrl: './sss.component.html',
  styleUrls: ['./sss.component.css']
})
export class SSSComponent {
  view_ac = 'ac_-1' ;       //ilk baş hepsi kapalı
  
  sorular?:Sorular[];
  
  constructor(private http: HttpClient) {}
  
  // ASP_NET_CORE_API = https://localhost:7263/api/Soru
  ngOnInit():void{
    this.http.get<Sorular[]>('http://localhost:5000/getSSS').subscribe(data => {
        this.sorular = data;
    })  
  }
  

  changeAccordion(ac:any){
    if (this.view_ac == ac){        // Eğer açık olan ise kapat
      this.view_ac = 'ac_-1';   
    }
    else{                           // Eğer açık olan değilse aç
      this.view_ac = ac;
    }
     
    
  }
}
