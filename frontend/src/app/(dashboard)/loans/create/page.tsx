'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import axiosInstance from '@/lib/api/axios';
import type { LoanFormData } from '@/lib/types/loan';

const schema = yup.object({
  applicant_name: yup.string().required('Applicant name is required'),
  amount: yup
    .number()
    .required('Amount is required')
    .positive('Amount must be positive')
    .max(1000000, 'Amount cannot exceed $1,000,000'),
  interest_rate: yup
    .number()
    .required('Interest rate is required')
    .min(0, 'Interest rate cannot be negative')
    .max(100, 'Interest rate cannot exceed 100%'),
  term_months: yup
    .number()
    .required('Loan term is required')
    .min(1, 'Term must be at least 1 month')
    .max(60, 'Term cannot exceed 60 months'),
}).required();

export default function CreateLoanPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoanFormData>({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data: LoanFormData) => {
    setLoading(true);
    setError('');

    try {
      await axiosInstance.post('/loan-applications/', data);
      router.push('/dashboard/loans');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create loan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Create New Loan</h1>
          <p className="mt-1 text-sm text-gray-500">
            Fill out the form below to create a new loan application.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label
              htmlFor="applicant_name"
              className="block text-sm font-medium text-gray-700"
            >
              Applicant Name
            </label>
            <input
              type="text"
              {...register('applicant_name')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {errors.applicant_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.applicant_name.message}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="amount"
              className="block text-sm font-medium text-gray-700"
            >
              Loan Amount ($)
            </label>
            <input
              type="number"
              step="0.01"
              {...register('amount')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {errors.amount && (
              <p className="mt-1 text-sm text-red-600">
                {errors.amount.message}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="interest_rate"
              className="block text-sm font-medium text-gray-700"
            >
              Interest Rate (%)
            </label>
            <input
              type="number"
              step="0.01"
              {...register('interest_rate')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {errors.interest_rate && (
              <p className="mt-1 text-sm text-red-600">
                {errors.interest_rate.message}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="term_months"
              className="block text-sm font-medium text-gray-700"
            >
              Term (Months)
            </label>
            <input
              type="number"
              {...register('term_months')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {errors.term_months && (
              <p className="mt-1 text-sm text-red-600">
                {errors.term_months.message}
              </p>
            )}
          </div>

          {error && (
            <div className="text-red-600 text-sm">{error}</div>
          )}

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {loading ? 'Creating...' : 'Create Loan'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 