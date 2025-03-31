# Complete System Architecture Diagram

```mermaid
graph TD
    Client((Client)) --> CloudFront[CloudFront CDN]
    CloudFront --> S3[S3 Static Website]
    CloudFront --> LambdaURL[Lambda Function URL]

    subgraph "Frontend System"
        S3 --> SvelteApp[SvelteKit Application]
        SvelteApp --> Components[UI Components]
        Components --> MapComponent[MapRoads]
        Components --> FilterComponent[SpeedFilter]
        Components --> ChartComponent[SpeedPieChart]
        
        SvelteApp --> StoreLayer[Svelte Stores]
        StoreLayer --> RoadsStore[roadsStore.ts]
        
        SvelteApp --> ExternalLibs[External Libraries]
        ExternalLibs --> Leaflet[Leaflet.js]
        ExternalLibs --> ChartJS[Chart.js]
        ExternalLibs --> Tailwind[TailwindCSS]
    end

    subgraph "Backend System"
        LambdaURL --> FastAPI[FastAPI Application]
        FastAPI --> RoadsRouter[roads.py Router]
        FastAPI --> StatsRouter[stats.py Router]
        
        RoadsRouter --> DBLayer[Database Layer]
        StatsRouter --> DBLayer
        
        DBLayer --> SQLAlchemy[SQLAlchemy ORM]
        SQLAlchemy --> PostgreSQL[(PostgreSQL + PostGIS)]
        
        RoadsRouter --> GlobalCache[Global Cache]
    end

    subgraph "CI/CD System"
        GitHub[GitHub Repository] --> FrontendCI[Frontend CI/CD]
        GitHub --> BackendCI[Backend CI/CD]
        
        FrontendCI --> FrontendTests[Vitest]
        FrontendCI --> FrontendBuild[Build Process]
        FrontendBuild --> S3Deploy[Deploy to S3]
        
        BackendCI --> BackendTests[Pytest]
        BackendCI --> ServerlessFramework[Serverless Framework]
        ServerlessFramework --> LambdaDeploy[Deploy to Lambda]
    end

    RoadsStore <--> APIClient[API Client]
    APIClient <--> LambdaURL
```

## Complete System Data Flow Diagram

```mermaid
sequenceDiagram
    participant User as User
    participant UI as UI Components
    participant Store as Svelte Store
    participant Cache as Frontend Cache
    participant API as API Client
    participant Backend as FastAPI Backend
    participant DBCache as Backend Cache
    participant DB as PostgreSQL/PostGIS

    User->>UI: Interaction (click/filter)
    UI->>Store: Trigger state update
    
    alt Speed filtering
        Store->>Store: Update speed filter conditions
        Store->>Cache: Check if corresponding data exists in cache
        
        alt Cache hit
            Cache-->>Store: Return cached data
        else Cache miss
            Store->>API: Request road data for specific speed
            API->>Backend: HTTP request /roads?max_speed=X
            
            Backend->>DBCache: Check backend cache
            
            alt Backend cache hit
                DBCache-->>Backend: Return cached data
            else Backend cache miss
                Backend->>DB: SQL query to get road data
                DB-->>Backend: Return query results
                Backend->>Backend: Convert to GeoJSON format
                Backend->>DBCache: Update cache
            end
            
            Backend-->>API: Return GeoJSON data (GZip compressed)
            API-->>Store: Parse response data
            Store->>Cache: Update frontend cache
        end
    else Map interaction
        UI->>UI: Update visible area
        UI->>Store: Request data within visible area
        Store->>UI: Provide filtered data
    end
    
    Store->>UI: Update UI components
    UI->>User: Display updated interface
```

## System Key Integration Points Description

### Frontend-Backend Integration Points

1. **API Interface Layer**
   - **Function URL Endpoint**: Direct HTTP endpoint provided by Lambda function
   - **GeoJSON Data Format**: Standard format for geographic data transmission between frontend and backend
   - **GZip Compression**: Compression mechanism to reduce data transfer volume

2. **Cache Strategy Coordination**
   - **Frontend Cache**: Cache previously requested data to avoid repeated requests
   - **Backend Cache**: Cache database query results to improve response speed
   - **Speed-based Cache Keys**: Common strategy of using speed values as cache keys

3. **Data Lazy Loading Mechanism**
   - **Frontend Visible Area Filtering**: Only process data within the map's visible area
   - **Backend Data Volume Limitation**: Control the maximum number of records returned each time

### Deployment and CI/CD Integration

1. **Branch Strategy**
   - **fprod Branch**: Triggers frontend deployment process
   - **bprod Branch**: Triggers backend deployment process

2. **Environment Configuration**
   - **.env.dev/.env.prod**: Configuration files for different environments
   - **GitHub Secrets**: Store sensitive configuration information

3. **Automated Testing**
   - **Frontend Testing**: Component testing using Vitest
   - **Backend Testing**: API and data access testing using Pytest