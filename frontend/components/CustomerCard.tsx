import React from 'react';
import { User, Phone, Mail, MapPin, Calendar, Edit, Trash2 } from 'lucide-react';
import { Customer, CustomerCardProps } from '@/types';
import Card from './ui/Card';
import Button from './ui/Button';

const CustomerCard: React.FC<CustomerCardProps> = ({
  customer,
  onEdit,
  onDelete,
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR');
  };

  const formatPhone = (phone: string) => {
    return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
  };

  return (
    <Card hover className="relative">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-accent-100 rounded-full flex items-center justify-center">
            <User className="w-6 h-6 text-accent-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-900">{customer.name}</h3>
            <p className="text-sm text-slate-500">ID: {customer.customer_id}</p>
          </div>
        </div>
        <div className="flex space-x-2">
          {onEdit && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(customer)}
              className="p-2"
            >
              <Edit className="w-4 h-4" />
            </Button>
          )}
          {onDelete && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(customer.id)}
              className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center space-x-3">
          <Phone className="w-4 h-4 text-slate-400" />
          <span className="text-sm text-slate-700">
            {formatPhone(customer.phone)}
          </span>
        </div>

        {customer.email && (
          <div className="flex items-center space-x-3">
            <Mail className="w-4 h-4 text-slate-400" />
            <span className="text-sm text-slate-700">{customer.email}</span>
          </div>
        )}

        {customer.birth_date && (
          <div className="flex items-center space-x-3">
            <Calendar className="w-4 h-4 text-slate-400" />
            <span className="text-sm text-slate-700">
              {formatDate(customer.birth_date)}
            </span>
          </div>
        )}

        {customer.address && (
          <div className="flex items-start space-x-3">
            <MapPin className="w-4 h-4 text-slate-400 mt-0.5" />
            <span className="text-sm text-slate-700 flex-1">{customer.address}</span>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-slate-200">
        <div className="flex justify-between text-xs text-slate-500">
          <span>등록일: {formatDate(customer.created_at)}</span>
          {customer.updated_at && (
            <span>수정일: {formatDate(customer.updated_at)}</span>
          )}
        </div>
      </div>
    </Card>
  );
};

export default CustomerCard;