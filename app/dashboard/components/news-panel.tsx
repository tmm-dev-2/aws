export function NewsPanel({ news }) {
    if (!news) return null;
  
    return (
      <div className="bg-[#252526] rounded-lg p-4 h-[600px] overflow-auto">
        <h2 className="text-xl font-semibold mb-4">Market News</h2>
        <div className="space-y-4">
          {news.map((item, index) => (
            <div key={index} className="border-b border-[#2a2a2a] pb-4">
              <h3 className="font-medium mb-2 hover:text-blue-400 cursor-pointer">
                {item.title}
              </h3>
              <p className="text-sm text-gray-400">{item.description}</p>
              <div className="flex justify-between mt-2 text-xs text-gray-500">
                <span>{item.source.name}</span>
                <span>{new Date(item.publishedAt).toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }
  