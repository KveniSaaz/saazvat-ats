import { Routes } from '@angular/router';

export const routes: Routes = [
     {
    path:'',
    loadComponent:()=> import('./resume-upload/resume-upload').then(m=>m.ResumeUpload)
  },
];
