import { Component } from '@angular/core';

@Component({
  selector: 'app-hakkimizda',
  templateUrl: './hakkimizda.component.html',
  styleUrls: ['./hakkimizda.component.css']
})
export class HakkimizdaComponent {

    paragraf="Bizler Ege Üniversitesi Bilgisayar Mühendisliği 4.sınıf öğrencileri Deniz Dilbaz ve Diren Yiğit Ceran'ız. Bitirme Tezi kapsamında pek çok türe ev sahipliği yapan güzel ülkemizde nesli tükenmekte olan bitkilerin tanınırlığını artırmak ve tespini kolaylaştırmak için bir proje gerçekleştiriyoruz. Sizlerin sayesinde nesli tükenmekte olan bitkiler tespit edildiğinde yetkili mercilere bilgi geçilmesi sağlanacak ve nesli tükenme tehlikesi altında olan türlerin korunması için çalışmalar gerçekleştirilebilecek."

    name?: string;
    email?: string;
    message?: string;

    constructor() {}

    sendEmail() {
    const subject = 'İletişim Formu Mesajı';
    const body = `Ad Soyad: ${this.name}\n\nE-posta: ${this.email}\n\nMesaj: ${this.message}`;

    const mailtoLink = `mailto:d.e.n.i.z_dilbaz@hotmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoLink;
  }

  }
