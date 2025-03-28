import { reactive } from 'vue'

interface Course {
  course_code: string;
  day: string;
  time_start: string;
  time_end: string;
  location: string;
}

export const store = reactive({
  courses: [],
  issues: [],
  
  // Schedule analyzer state
  fallSchedule: null as File | null,
  winterSchedule: null as File | null,
  loading: false,
  analysisResult: null as { 
    courses: Course[], 
    cs_requirements: string[] 
  } | null,
  
  // Computed-like getters
  get canAnalyze() {
    return this.fallSchedule && this.winterSchedule;
  },
  
  // Methods
  setFallSchedule(file: File) {
    this.fallSchedule = file;
  },
  
  setWinterSchedule(file: File) {
    this.winterSchedule = file;
  },
  
  async analyzeSchedules() {
    this.loading = true;
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    this.analysisResult = {
      courses: [
        {
          course_code: 'STAT 362',
          day: 'Friday',
          time_start: '11:30AM',
          time_end: '12:30PM',
          location: 'Biosciences Complex 1102'
        },
        {
          course_code: 'CISC 324',
          day: 'Monday',
          time_start: '2:30PM',
          time_end: '4:00PM',
          location: 'Jeffery Hall 155'
        }
      ],
      cs_requirements: [
        'Missing required course CISC 235',
        'Consider taking CISC 352 as a technical elective'
      ]
    };
    
    this.loading = false;
    return this.analysisResult;
  },
  
  resetState() {
    this.fallSchedule = null;
    this.winterSchedule = null;
    this.analysisResult = null;
    this.loading = false;
  }
})
