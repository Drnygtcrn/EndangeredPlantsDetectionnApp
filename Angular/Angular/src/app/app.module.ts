import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './Components/navbar/navbar.component';
import { HakkimizdaComponent } from './Components/hakkimizda/hakkimizda.component';
import { TukenmektelerComponent } from './Components/tukenmekteler/tukenmekteler.component';
import { SSSComponent } from './Components/sss/sss.component';
import { BannerComponent } from './Components/banner/banner.component';

import { MatExpansionModule } from '@angular/material/expansion';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';
import { AdminComponent } from './Components/admin/admin.component';
import { AnasayfaComponent } from './Components/anasayfa/anasayfa.component';
import { FooterComponent } from './Components/footer/footer.component';
import { HttpClientModule,HTTP_INTERCEPTORS } from '@angular/common/http';
import { CorsInterceptor } from 'src/interceptors/CorsInterceptor';
import { PopupComponent } from './Components/popup/popup.component';

import {MatDialogModule} from '@angular/material/dialog';
import { HaritaComponent } from './Components/harita/harita.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HakkimizdaComponent,
    TukenmektelerComponent,
    SSSComponent,
    BannerComponent,
    AdminComponent,
    AnasayfaComponent,
    FooterComponent,
    PopupComponent,
    HaritaComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    MatExpansionModule,
    BrowserAnimationsModule, 
    FormsModule,
    NgxPaginationModule,
    MatDialogModule
  ],
  providers: [
    {
      provide:HTTP_INTERCEPTORS,
      useClass: CorsInterceptor,
      multi:true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
