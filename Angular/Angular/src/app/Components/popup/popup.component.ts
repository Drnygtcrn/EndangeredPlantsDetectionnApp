import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Nesli } from 'src/app/Classes/Nesli';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.css']
})
export class PopupComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data:any, private Ref:MatDialogRef<PopupComponent>,private http:HttpClient){}

  tahmin:any;
  Isim?:any;
  Aciklama?:any;
  Fotograf?:any;
  ngOnInit(): void {
    this.tahmin = this.data.deger;
    this.Isim = this.data.Isim;
    this.Aciklama = this.data.Aciklama;
    this.Fotograf = this.data.Fotograf;
  }
  closePopup(){
    this.Ref.close();
  }








}
