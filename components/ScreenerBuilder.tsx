import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { ScreenerCondition } from '@/types/screener.types';

export const ScreenerBuilder = ({
  conditions,
  onConditionChange,
}: {
  conditions: ScreenerCondition[];
  onConditionChange: (conditions: ScreenerCondition[]) => void;
}) => {
  return (
    <div className="bg-gray-900 p-6 rounded-lg">
      <div className="flex items-center gap-4 mb-6">
        <h3 className="text-xl text-white font-semibold">Screener Conditions</h3>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md">
          Add Condition
        </button>
      </div>
      
      <DragDropContext onDragEnd={(result) => {
        // Handle drag end
      }}>
        <Droppable droppableId="conditions">
          {(provided) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="space-y-4"
            >
              {conditions.map((condition, index) => (
                <Draggable
                  key={condition.id}
                  draggableId={condition.id}
                  index={index}
                >
                  {(provided) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      className="bg-gray-800 p-4 rounded-md"
                    >
                      {/* Condition content */}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
};
