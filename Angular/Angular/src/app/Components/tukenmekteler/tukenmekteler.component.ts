import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Nesli } from 'src/app/Classes/Nesli';




@Component({
  selector: 'app-tukenmekteler',
  templateUrl: './tukenmekteler.component.html',
  styleUrls: ['./tukenmekteler.component.css']
})
export class TukenmektelerComponent {


  nesliListesi: Nesli[] = [];

  constructor(private http: HttpClient) { }
  ngOnInit():void{
    this.http.get<Nesli[]>('http://localhost:5000/getNesli').subscribe(data => {
        this.nesliListesi = data;
    })  
  }

  p:number =1;
  sayfadakiSayi:number =3;
  //toplam:number = this.bitkiler.length;
  toplam:number = this.nesliListesi.length;

  public filtre!:string ;

  

}
