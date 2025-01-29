// MessageActions component code...
export function MessageActions({ message }) {
    const [showReportModal, setShowReportModal] = useState(false);
    
    const reportReasons = [
      'Abuse',
      'Fake News',
      'Malicious Intent',
      'Spam',
      'Other'
    ];
  
    return (
      <Menu>
        <MenuTrigger>
          <MoreVertical className="h-4 w-4" />
        </MenuTrigger>
        
        <MenuContent>
          <MenuItem onSelect={() => setShowReportModal(true)}>
            Report
          </MenuItem>
        </MenuContent>
  
        {showReportModal && (
          <ReportModal
            onSubmit={handleReport}
            reasons={reportReasons}
            onClose={() => setShowReportModal(false)}
          />
        )}
      </Menu>
    );
  }
  