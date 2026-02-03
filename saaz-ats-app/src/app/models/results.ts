export interface Candidate {
  name: string;
  emailId: string;
  mobileNo: string;
  nativePlace: string;
}

export interface ResumeResult {
  filename: string;
  candidate: Candidate;
  ats_score: number;
  matched: string[];
  missing: string[];
}

export interface AnalyzeResponse {
  results: ResumeResult[];
}