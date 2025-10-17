import React, { useState, useEffect } from 'react';
import { Users, ChevronDown } from 'lucide-react';
import { usersApi } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const UserSelector = ({ selectedUser, onUserSelect }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await usersApi.getAll();
      setUsers(response.data);
      if (response.data.length > 0 && !selectedUser) {
        onUserSelect(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch users:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner size="sm" text="" />;
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between bg-white border-2 border-gray-200 rounded-lg px-4 py-3 hover:border-primary-500 transition-colors"
      >
        <div className="flex items-center space-x-3">
          <Users className="h-5 w-5 text-primary-600" />
          <div className="text-left">
            <p className="text-sm text-gray-500">Shopping as</p>
            <p className="font-semibold text-gray-900">
              {selectedUser?.name || 'Select a user'}
            </p>
          </div>
        </div>
        <ChevronDown className={`h-5 w-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown */}
          <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-xl border border-gray-200 z-20 max-h-96 overflow-y-auto">
            {users.map((user) => (
              <button
                key={user.id}
                onClick={() => {
                  onUserSelect(user);
                  setIsOpen(false);
                }}
                className={`w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0 ${
                  selectedUser?.id === user.id ? 'bg-primary-50' : ''
                }`}
              >
                <p className="font-medium text-gray-900">{user.name}</p>
                <p className="text-sm text-gray-500">{user.email}</p>
                {user.preferences && (
                  <div className="mt-1 flex flex-wrap gap-1">
                    {user.preferences.interests?.slice(0, 3).map((interest, idx) => (
                      <span
                        key={idx}
                        className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded"
                      >
                        {interest}
                      </span>
                    ))}
                  </div>
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default UserSelector;