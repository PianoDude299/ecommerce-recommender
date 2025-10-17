import React from 'react';
import { AlertCircle } from 'lucide-react';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
        <div className="flex items-start">
          <AlertCircle className="h-6 w-6 text-red-600 mr-3 flex-shrink-0" />
          <div>
            <h3 className="text-lg font-semibold text-red-900 mb-2">
              Something went wrong
            </h3>
            <p className="text-red-700 mb-4">{message}</p>
            {onRetry && (
              <button
                onClick={onRetry}
                className="btn-primary"
              >
                Try Again
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;