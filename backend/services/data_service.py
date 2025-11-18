"""
Data Service Module
Handles querying and aggregating ARGO oceanographic data from the database
"""
from typing import Dict, List, Any, Optional
from sqlalchemy import func, and_, desc
from db.session import SessionLocal
from db.models import ArgoRecord
from datetime import datetime

class DataService:
    """Service for querying ARGO float data"""
    
    def __init__(self):
        self.session = None
    
    def _get_session(self):
        """Get database session"""
        if not self.session:
            self.session = SessionLocal()
        return self.session
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Get overall statistics about the ARGO dataset
        
        Returns:
            Dictionary containing dataset statistics
        """
        session = self._get_session()
        
        try:
            # Count total records
            total = session.query(func.count(ArgoRecord.id)).scalar() or 0
            
            if total == 0:
                return {
                    "total_records": 0,
                    "message": "No data available. Please run fetch_argovis.py to ingest data."
                }
            
            # Get unique floats
            floats = session.query(ArgoRecord.platform).distinct().all()
            float_list = [f[0] for f in floats if f[0]]
            
            # Date range
            min_date = session.query(func.min(ArgoRecord.time)).scalar()
            max_date = session.query(func.max(ArgoRecord.time)).scalar()
            
            # Depth range
            min_depth = session.query(func.min(ArgoRecord.depth)).scalar()
            max_depth = session.query(func.max(ArgoRecord.depth)).scalar()
            
            # Temperature range (excluding nulls)
            temp_stats = session.query(
                func.min(ArgoRecord.temperature),
                func.max(ArgoRecord.temperature),
                func.avg(ArgoRecord.temperature)
            ).filter(ArgoRecord.temperature.isnot(None)).first()
            
            # Salinity range (excluding nulls)
            sal_stats = session.query(
                func.min(ArgoRecord.salinity),
                func.max(ArgoRecord.salinity),
                func.avg(ArgoRecord.salinity)
            ).filter(ArgoRecord.salinity.isnot(None)).first()
            
            # Geographic bounds
            lat_bounds = session.query(
                func.min(ArgoRecord.latitude),
                func.max(ArgoRecord.latitude)
            ).first()
            
            lon_bounds = session.query(
                func.min(ArgoRecord.longitude),
                func.max(ArgoRecord.longitude)
            ).first()
            
            return {
                "total_records": total,
                "floats": float_list,
                "float_count": len(float_list),
                "date_range": {
                    "min": min_date.isoformat() if min_date else None,
                    "max": max_date.isoformat() if max_date else None
                },
                "depth_range": {
                    "min": float(min_depth) if min_depth else None,
                    "max": float(max_depth) if max_depth else None,
                    "unit": "dbar"
                },
                "temperature": {
                    "min": round(float(temp_stats[0]), 2) if temp_stats[0] else None,
                    "max": round(float(temp_stats[1]), 2) if temp_stats[1] else None,
                    "avg": round(float(temp_stats[2]), 2) if temp_stats[2] else None,
                    "unit": "°C"
                },
                "salinity": {
                    "min": round(float(sal_stats[0]), 2) if sal_stats[0] else None,
                    "max": round(float(sal_stats[1]), 2) if sal_stats[1] else None,
                    "avg": round(float(sal_stats[2]), 2) if sal_stats[2] else None,
                    "unit": "PSU"
                },
                "geographic_bounds": {
                    "latitude": {
                        "min": float(lat_bounds[0]) if lat_bounds[0] else None,
                        "max": float(lat_bounds[1]) if lat_bounds[1] else None
                    },
                    "longitude": {
                        "min": float(lon_bounds[0]) if lon_bounds[0] else None,
                        "max": float(lon_bounds[1]) if lon_bounds[1] else None
                    }
                }
            }
        
        except Exception as e:
            print(f"Error getting stats: {e}")
            raise
    
    def query_records(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query ARGO records with optional filters
        
        Args:
            filters: Dictionary of filter parameters
                - min_depth, max_depth
                - min_temp, max_temp
                - min_sal, max_sal
                - platform
                - limit
        
        Returns:
            List of record dictionaries
        """
        session = self._get_session()
        
        query = session.query(ArgoRecord)
        
        # Apply filters
        if 'min_depth' in filters:
            query = query.filter(ArgoRecord.depth >= filters['min_depth'])
        if 'max_depth' in filters:
            query = query.filter(ArgoRecord.depth <= filters['max_depth'])
        
        if 'min_temp' in filters:
            query = query.filter(ArgoRecord.temperature >= filters['min_temp'])
        if 'max_temp' in filters:
            query = query.filter(ArgoRecord.temperature <= filters['max_temp'])
        
        if 'min_sal' in filters:
            query = query.filter(ArgoRecord.salinity >= filters['min_sal'])
        if 'max_sal' in filters:
            query = query.filter(ArgoRecord.salinity <= filters['max_sal'])
        
        if 'platform' in filters:
            query = query.filter(ArgoRecord.platform == filters['platform'])
        
        # Limit results
        limit = filters.get('limit', 100)
        query = query.order_by(desc(ArgoRecord.time)).limit(limit)
        
        records = query.all()
        
        return [
            {
                "id": r.id,
                "time": r.time.isoformat() if r.time else None,
                "latitude": float(r.latitude) if r.latitude else None,
                "longitude": float(r.longitude) if r.longitude else None,
                "depth": float(r.depth) if r.depth else None,
                "temperature": float(r.temperature) if r.temperature else None,
                "salinity": float(r.salinity) if r.salinity else None,
                "platform": r.platform
            }
            for r in records
        ]
    
    def get_relevant_context(self, user_query: str) -> Dict[str, Any]:
        """
        Get relevant ARGO data context for a user query
        
        Args:
            user_query: The user's question
        
        Returns:
            Dictionary with relevant data and statistics
        """
        query_lower = user_query.lower()
        
        # Get basic stats
        stats = self.get_dataset_stats()
        
        context = {
            "stats": stats,
            "sample_data": []
        }
        
        # Determine what kind of data to include
        filters = {}
        
        # Depth-related queries
        if any(word in query_lower for word in ['surface', 'shallow', 'top']):
            filters['max_depth'] = 50
            filters['limit'] = 20
        elif any(word in query_lower for word in ['deep', 'bottom', 'depth']):
            filters['min_depth'] = 500
            filters['limit'] = 20
        
        # Temperature queries
        if any(word in query_lower for word in ['warm', 'hot', 'temperature', 'temp']):
            filters['limit'] = 30
        
        # Get sample data
        try:
            if filters or 'sample' in query_lower or 'show' in query_lower:
                context["sample_data"] = self.query_records(filters if filters else {'limit': 20})
        except Exception as e:
            print(f"Error getting sample data: {e}")
        
        return context
    
    def get_temperature_profile(self, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get temperature vs depth profile
        
        Args:
            platform: Optional float ID to filter by
        
        Returns:
            List of depth/temperature pairs
        """
        session = self._get_session()
        
        query = session.query(
            ArgoRecord.depth,
            func.avg(ArgoRecord.temperature).label('avg_temp')
        ).filter(ArgoRecord.temperature.isnot(None))
        
        if platform:
            query = query.filter(ArgoRecord.platform == platform)
        
        query = query.group_by(ArgoRecord.depth).order_by(ArgoRecord.depth)
        
        results = query.all()
        
        return [
            {
                "depth": float(r.depth),
                "temperature": round(float(r.avg_temp), 2)
            }
            for r in results
        ]
    
    def __del__(self):
        """Close database session on cleanup"""
        if self.session:
            self.session.close()
