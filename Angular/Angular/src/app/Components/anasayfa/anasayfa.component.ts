import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { PopupComponent } from '../popup/popup.component';
import { Nesli } from 'src/app/Classes/Nesli';

@Component({
  selector: 'app-anasayfa',
  templateUrl: './anasayfa.component.html',
  styleUrls: ['./anasayfa.component.css']
})
export class AnasayfaComponent {
  file: any;
  tahmin?: any;
  imgURL?: any;
  Isim?:any;
  Aciklama?:any;
  Fotograf?:any;
  Latin?:any;
  olmayan = 'Nesli Tükenmemekte Olan Bitkiler';

  constructor(private http: HttpClient,private matdialog:MatDialog) {}

  
  ngOnInit() {
    
  }
  
  
  onFileSelected(event: any): void {
    this.file = event.target.files[0];
  }

  async onUpload() {
    if (!this.file) {
      console.log('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.file, this.file.name);

    await this.http.post<any>('http://localhost:5000/predict', formData).subscribe(
      (res) => {
        this.tahmin = res.result;
        this.Isim = res.Isim;
        this.Aciklama = res.Aciklama;
        this.Fotograf = res.Fotograf;
        this.Latin = res.Latin;
        this.openPopUp(this.tahmin,this.Isim,this.Aciklama,this.Fotograf);
        console.log(res.Fotograf);

        if (navigator.geolocation && this.tahmin !=this.olmayan) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              const longitude = position.coords.longitude;
              const latitude = position.coords.latitude;
    
              const data = {
                latitude: latitude,
                longitude: longitude,
                isim: res.Latin,
                fotograf: res.Fotograf
                
              };
              console.log(data);

              this.http.post<any>('http://localhost:5000/postkonum', data).subscribe(
                (response) => {
                  console.log(response);
                 
                },
                (error) => {
                  console.log(error);
                  
                }
              );
            },
            (error) => {
              console.log(error);
              
            }
          );
        } else {
          console.log("No support for geolocation");
        }    



      },
      (error) => {
        console.log(error);
      }
    );
  }

  openPopUp(taho:any,isim:any,acik:any,foto:any){
    this.matdialog.open(PopupComponent,{width:'%100',height:'700px',
    data:{deger:taho,
          Isim:isim,
          Aciklama:acik,
          Fotograf:foto},
    });
  }

  konum: any ={
    latitude: '',
    longitude: ''
  }

/*
  getLocation(){
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const longitude = position.coords.longitude;
          const latitude = position.coords.latitude;

          const data = {
            latitude: latitude,
            longitude: longitude
          };

          this.http.post<any>('http://127.0.0.1:5000/konum', data).subscribe(
            (response) => {
              console.log(response);
            
            },
            (error) => {
              console.log(error);
             
            }
          );
        },
        (error) => {
          console.log(error);
     
        }
      );
    } else {
      console.log("No support for geolocation");
    }
  }*/

  
}
