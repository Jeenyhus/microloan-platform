'use client';

import { useAuth } from '@/lib/context/AuthContext';
import { useState, useEffect } from 'react';
import axiosInstance from '@/lib/api/axios';

interface DashboardStats {
  totalLoans: number;
  activeLoans: number;
  totalRepayments: number;
  pendingRepayments: number;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axiosInstance.get('/dashboard/stats/');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div>Loading stats...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="rounded-md bg-indigo-500 p-3">
                  {/* Icon */}
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Loans
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats?.totalLoans || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        {/* Add more stat cards here */}
      </div>

      {/* Add more dashboard content here */}
    </div>
  );
} 