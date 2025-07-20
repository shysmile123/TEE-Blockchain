export interface DataCollection {
    id: string;
    timestamp: Date;
    data: any;
    signature: string;
}

export interface VerificationResult {
    isValid: boolean;
    message: string;
    timestamp: Date;
}