import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AnalyzeResponse } from '../models/results';

@Injectable({
  providedIn: 'root',
})
export class ResumeUploadService {
   private filesSubject = new BehaviorSubject<File[]>([]);
  files$ = this.filesSubject.asObservable();
  

  constructor(private http: HttpClient) {}

  setFiles(files: File[]) {
    this.filesSubject.next(files);
  }

  getFiles() {
    return this.filesSubject.value;
  }

  uploadResumes(jd: string, skills: string, files: File[]) {
    const formData = new FormData();
    formData.append("jd", jd);
    formData.append("skills", skills);

   
    files.forEach(file => formData.append("resumes", file));
    console.log(formData);
    

      return this.http.post<AnalyzeResponse>(
    "http://localhost:8000/analyze",
    formData
  );
  }
}
