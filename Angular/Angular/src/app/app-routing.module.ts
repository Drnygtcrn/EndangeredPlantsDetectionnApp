import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TukenmektelerComponent } from './Components/tukenmekteler/tukenmekteler.component';
import { SSSComponent } from './Components/sss/sss.component';
import { HakkimizdaComponent } from './Components/hakkimizda/hakkimizda.component';
import { AdminComponent } from './Components/admin/admin.component';
import { AnasayfaComponent } from './Components/anasayfa/anasayfa.component';
import { HaritaComponent } from './Components/harita/harita.component';

const routes: Routes = [
  {path:"TukenmekteOlanlar",component:TukenmektelerComponent},
  {path:"sss",component:SSSComponent},
  {path:"hakkimizda",component:HakkimizdaComponent},
  {path:"admin",component:AdminComponent},
  {path:'',pathMatch:'full',component:AnasayfaComponent},
  {path:'tespitler',component:HaritaComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
