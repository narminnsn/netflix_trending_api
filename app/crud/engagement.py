from typing import Optional
from sqlalchemy.orm import Session
from datetime import date
from app.models import ViewSummary, Movie, Season, TVShow

class CRUDEngagement:

    def get_engagement_timeline(
        self,
        db: Session,
        id_: int,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> Optional[dict]:
        """
        Given a title id (movie or season), returns the weekly/semi-annual engagement timeline.
        """
        # We could add a "type" argument to specify whether the ID belongs to a movie or a season,
        # because the same ID values can appear in both movies and seasons, which may cause confusion.
        # For now, we handle this by sequentially checking: first we look for the ID in movies,
        # and if not found, then we check in seasons.


        # 1. Check if id exists in Movie
        movie = db.query(Movie).filter(Movie.id == id_).first()
        if movie:
            # Query ViewSummary for movie entries matching id and filters
            query = db.query(
                ViewSummary.start_date,
                ViewSummary.hours_viewed,
                ViewSummary.views,
                ViewSummary.view_rank,
            ).filter(
                ViewSummary.movie_id == id_
            )
            if from_date:
                query = query.filter(ViewSummary.start_date >= from_date)
            if to_date:
                query = query.filter(ViewSummary.start_date <= to_date)

            query = query.order_by(ViewSummary.start_date.asc())
            records = query.all()

            # Debug print to confirm records count
            print(f"Movie ID {id_} timeline records found: {len(records)}")

            timeline = [
                {
                    "start_date": r.start_date.isoformat(),
                    "hours_viewed": r.hours_viewed,
                    "views": r.views,
                    "view_rank": r.view_rank,
                }
                for r in records
            ]

            return {
                "id": movie.id,
                "type": "movie",
                "title": movie.title,
                "timeline": timeline,
            }

        # 2. Else check if id exists in Season
        season = (
            db.query(Season)
            .join(TVShow, TVShow.id == Season.tv_show_id)
            .filter(Season.id == id_)
            .first()
        )
        if season:
            # Query ViewSummary for season entries matching id and filters
            query = db.query(
                ViewSummary.start_date,
                ViewSummary.hours_viewed,
                ViewSummary.views,
                ViewSummary.view_rank,
            ).filter(
                ViewSummary.season_id == id_
            )
            if from_date:
                query = query.filter(ViewSummary.start_date >= from_date)
            if to_date:
                query = query.filter(ViewSummary.start_date <= to_date)

            query = query.order_by(ViewSummary.start_date.asc())
            records = query.all()

            timeline = [
                {
                    "start_date": r.start_date.isoformat(),
                    "hours_viewed": r.hours_viewed,
                    "views": r.views,
                    "view_rank": r.view_rank,
                }
                for r in records
            ]

            full_title = f"{season.tv_show.title} •S{season.season_number}"
            print()
            return {
                "id": season.id,
                "type": "season",
                "title": full_title,
                "timeline": timeline,
            }

        # 3. If no movie or season found with this id, return None
        return None