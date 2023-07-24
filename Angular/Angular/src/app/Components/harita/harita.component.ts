import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Konum } from 'src/app/Classes/Konum';

@Component({
  selector: 'app-harita',
  templateUrl: './harita.component.html',
  styleUrls: ['./harita.component.css']
})
export class HaritaComponent{
 

  constructor(private http: HttpClient) {}

  seciliSehir?:string;
  konumListesi: Konum[] = [];

  ngOnInit() {
    this.http.get<Konum[]>('http://localhost:5000/getkonum').subscribe(data => {
         this.konumListesi = data;
     })
  }
  
  showCoordinates: boolean = false;
  

   
   toggleCoordinates() {
     this.showCoordinates = !this.showCoordinates;
   }



  p:number =1;
  sayfadakiSayi:number =3;

  toplam:number = this.konumListesi.length;

  public filtre!:string ;
  
  secilenSehir(sehir:string){
    if(sehir == 'Eskişehir'){
      this.seciliSehir = 'Eskisehir';
      console.log(this.seciliSehir);
    }
    else{
      this.seciliSehir = sehir;
    }  
    
    const url = `http://localhost:5000/getkonumSehir/${this.seciliSehir}`;
    this.http.get<Konum[]>(url).subscribe(
      (response) => {
        this.konumListesi = response
        console.log(response);
      },
      (error) => {
        // Hata durumunda yapılacak işlemler
        console.error(error);
      }
    );


  }
  
  




}
