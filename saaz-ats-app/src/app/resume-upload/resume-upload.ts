import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { FileUploadModule } from 'primeng/fileupload';

import { InputTextModule } from 'primeng/inputtext';
import { TextareaModule } from 'primeng/textarea';

@Component({
  selector: 'app-resume-upload',
  imports: [CommonModule,FormsModule,ButtonModule, FileUploadModule,
    TextareaModule,
    InputTextModule,],
  templateUrl: './resume-upload.html',
  styleUrl: './resume-upload.scss',
})
export class ResumeUpload {
 jobDescription = "";
  skills = "";
  selectedFile: any;
  result: any;

  constructor(private http: HttpClient) {}

  onFileChange(event: any) {
    this.selectedFile = event.target.files[0];
  }

  analyze() {
    const formData = new FormData();
    formData.append("jd", this.jobDescription);
    formData.append("skills", this.skills);
    formData.append("resume", this.selectedFile);

    this.http.post("http://127.0.0.1:8000/analyze", formData)
      .subscribe((res: any) => {
        this.result = res;
      });
  }

}
