// WarningBanner component code...
export function WarningBanner({ warningCount }) {
    return warningCount > 0 ? (
      <div className="bg-red-500/10 border border-red-500 p-4 rounded-lg mb-4">
        <p className="text-red-500">
          Warning: You have received {warningCount} reports. 
          {warningCount >= 3 && ' You need to apologize to continue messaging.'}
        </p>
      </div>
    ) : null;
  }
  